"""Constraint-Aware Plan Optimization Engine."""
import json
from typing import Dict, Any, List
from utils.llm_client import llm_client
from config.prompts import SYSTEM_ROLE

PLAN_GENERATION_PROMPT = """
Generate {num_plans} different action plans for achieving the user's goal.

User Input: {user_input}
Intent: {intent_data}
Constraints: {constraint_data}

Each plan should:
1. Take a different strategic approach
2. Optimize for different priorities (speed, cost, quality, risk)
3. Be realistic and actionable

Return JSON:
{{
    "plans": [
        {{
            "plan_id": "unique_id",
            "strategy": "speed-optimized/cost-optimized/quality-optimized/balanced",
            "description": "overall approach",
            "steps": [
                {{
                    "step_number": 1,
                    "title": "step title",
                    "description": "what to do",
                    "estimated_time": "time estimate",
                    "estimated_cost": "cost if applicable",
                    "resources_needed": ["list"],
                    "risk_level": "low/medium/high"
                }}
            ],
            "total_time": "overall time",
            "total_cost": "overall cost",
            "success_probability": 0.0-1.0,
            "key_advantages": ["list"],
            "key_disadvantages": ["list"]
        }}
    ]
}}
"""

PLAN_SCORING_PROMPT = """
Score each plan against the user's constraints and priorities.

Plans: {plans}
Constraints: {constraints}
Priorities: {priorities}

Scoring criteria:
1. Time feasibility (does it fit timeline?)
2. Resource feasibility (within budget/resources?)
3. Skill match (matches user's skill level?)
4. Risk level (acceptable risk?)
5. Success probability
6. Alignment with priorities

Return JSON:
{{
    "scored_plans": [
        {{
            "plan_id": "id",
            "scores": {{
                "time_feasibility": 0.0-1.0,
                "resource_feasibility": 0.0-1.0,
                "skill_match": 0.0-1.0,
                "risk_acceptability": 0.0-1.0,
                "success_probability": 0.0-1.0,
                "priority_alignment": 0.0-1.0
            }},
            "overall_score": 0.0-1.0,
            "rank": 1,
            "recommendation": "highly recommended/recommended/acceptable/not recommended",
            "reasoning": "why this score"
        }}
    ],
    "optimal_plan_id": "id of best plan"
}}
"""

class PlanOptimizer:
    """Generates and optimizes multiple action plans."""
    
    def generate_multiple_plans(
        self,
        user_input: str,
        intent_data: Dict[str, Any],
        constraint_data: Dict[str, Any],
        num_plans: int = 3
    ) -> Dict[str, Any]:
        """
        Generate multiple candidate plans with different strategies.
        
        Args:
            user_input: Original input
            intent_data: Extracted intent
            constraint_data: Constraints
            num_plans: Number of plans to generate
            
        Returns:
            Multiple plans
        """
        prompt = PLAN_GENERATION_PROMPT.format(
            num_plans=num_plans,
            user_input=user_input,
            intent_data=json.dumps(intent_data, indent=2),
            constraint_data=json.dumps(constraint_data, indent=2)
        )
        
        result = llm_client.generate_json(
            system_prompt=SYSTEM_ROLE,
            user_prompt=prompt,
            temperature=0.8,
            max_tokens=3000
        )
        
        result.setdefault("plans", [])
        
        return result
    
    def score_plans(
        self,
        plans: List[Dict[str, Any]],
        constraints: Dict[str, Any],
        priorities: List[str] = None
    ) -> Dict[str, Any]:
        """
        Score each plan against constraints and priorities.
        
        Args:
            plans: List of generated plans
            constraints: User constraints
            priorities: User priorities (e.g., ["speed", "low-cost"])
            
        Returns:
            Scored and ranked plans
        """
        if priorities is None:
            priorities = ["balanced"]
        
        prompt = PLAN_SCORING_PROMPT.format(
            plans=json.dumps(plans, indent=2),
            constraints=json.dumps(constraints, indent=2),
            priorities=json.dumps(priorities)
        )
        
        result = llm_client.generate_json(
            system_prompt=SYSTEM_ROLE,
            user_prompt=prompt,
            temperature=0.6,
            max_tokens=2000
        )
        
        result.setdefault("scored_plans", [])
        result.setdefault("optimal_plan_id", "")
        
        return result
    
    def select_optimal_plan(
        self,
        scored_plans: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Select the optimal plan based on scores.
        
        Args:
            scored_plans: Plans with scores
            
        Returns:
            Optimal plan
        """
        if not scored_plans:
            return {}
        
        # Sort by overall score
        sorted_plans = sorted(
            scored_plans,
            key=lambda p: p.get("overall_score", 0),
            reverse=True
        )
        
        return sorted_plans[0] if sorted_plans else {}
    
    def compare_plans(
        self,
        plans: List[Dict[str, Any]],
        scored_plans: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate a comparison matrix of all plans.
        
        Args:
            plans: Original plans
            scored_plans: Scored plans
            
        Returns:
            Comparison data
        """
        comparison = {
            "criteria": [
                "Time Required",
                "Cost",
                "Success Probability",
                "Risk Level",
                "Skill Required",
                "Overall Score"
            ],
            "plans_comparison": []
        }
        
        for plan, scored in zip(plans, scored_plans):
            comparison["plans_comparison"].append({
                "plan_id": plan.get("plan_id"),
                "strategy": plan.get("strategy"),
                "metrics": {
                    "time": plan.get("total_time"),
                    "cost": plan.get("total_cost"),
                    "success_prob": plan.get("success_probability"),
                    "risk": plan.get("steps", [{}])[0].get("risk_level", "medium"),
                    "overall_score": scored.get("overall_score")
                }
            })
        
        return comparison

plan_optimizer = PlanOptimizer()
