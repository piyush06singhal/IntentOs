"""Action plan generation engine."""
import json
from typing import Dict, Any, List, Optional
from utils.llm_client import llm_client
from config.prompts import (
    SYSTEM_ROLE,
    ACTION_PLAN_PROMPT,
    ALTERNATIVE_STRATEGIES_PROMPT
)

class Planner:
    """Generates actionable plans based on intent and constraints."""
    
    def generate_plan(
        self,
        user_input: str,
        intent_data: Dict[str, Any],
        constraint_data: Dict[str, Any],
        clarification_responses: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Generate a detailed action plan.
        
        Args:
            user_input: Original user input
            intent_data: Extracted intent
            constraint_data: Extracted constraints
            clarification_responses: User responses to clarification questions
            
        Returns:
            Dictionary containing:
                - plan: List of steps
                - total_estimated_time: Overall time estimate
                - critical_path: Critical steps
                - risks: Potential risks
                - success_metrics: Success criteria
        """
        clarifications = clarification_responses or {}
        
        prompt = ACTION_PLAN_PROMPT.format(
            user_input=user_input,
            intent_data=json.dumps(intent_data, indent=2),
            constraint_data=json.dumps(constraint_data, indent=2),
            clarification_responses=json.dumps(clarifications, indent=2)
        )
        
        result = llm_client.generate_json(
            system_prompt=SYSTEM_ROLE,
            user_prompt=prompt,
            temperature=0.7,
            max_tokens=3000
        )
        
        # Normalize
        result.setdefault("plan", [])
        result.setdefault("total_estimated_time", "Unknown")
        result.setdefault("critical_path", [])
        result.setdefault("risks", [])
        result.setdefault("success_metrics", [])
        
        return result
    
    def generate_alternatives(
        self,
        original_plan: Dict[str, Any],
        constraint_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate alternative strategies for different scenarios.
        
        Args:
            original_plan: The main action plan
            constraint_data: Extracted constraints
            
        Returns:
            List of alternative strategy dictionaries
        """
        prompt = ALTERNATIVE_STRATEGIES_PROMPT.format(
            original_plan=json.dumps(original_plan, indent=2),
            constraint_data=json.dumps(constraint_data, indent=2)
        )
        
        result = llm_client.generate_json(
            system_prompt=SYSTEM_ROLE,
            user_prompt=prompt,
            temperature=0.8,
            max_tokens=2000
        )
        
        return result.get("alternatives", [])
    
    def optimize_plan_for_constraint(
        self,
        plan: Dict[str, Any],
        constraint_type: str,
        constraint_value: str
    ) -> Dict[str, Any]:
        """
        Optimize an existing plan for a specific constraint.
        
        Args:
            plan: Original plan
            constraint_type: Type of constraint (e.g., "time", "skill")
            constraint_value: Constraint value
            
        Returns:
            Optimized plan
        """
        # This could be expanded for real-time plan optimization
        return plan

planner = Planner()
