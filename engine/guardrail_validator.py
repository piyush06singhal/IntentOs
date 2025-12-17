"""Hallucination & Contradiction Guardrail Layer."""
import json
from typing import Dict, Any, List, Tuple
from utils.llm_client import llm_client
from config.prompts import SYSTEM_ROLE

VALIDATION_PROMPT = """
Validate the generated plan against the original input and constraints for contradictions and hallucinations.

Original Input: {user_input}
Extracted Constraints: {constraints}
Generated Plan: {plan}

Check for:
1. Contradictions between plan and stated constraints
2. Hallucinated information not present in input
3. Logical inconsistencies within the plan
4. Unrealistic assumptions
5. Missing critical constraint considerations

Return JSON:
{{
    "is_valid": boolean,
    "confidence": 0.0-1.0,
    "issues": [
        {{
            "type": "contradiction/hallucination/inconsistency/unrealistic/missing",
            "severity": "critical/high/medium/low",
            "description": "what's wrong",
            "location": "where in the plan",
            "suggested_fix": "how to correct it"
        }}
    ],
    "critical_issues_count": 0,
    "recommendation": "approve/revise/reject"
}}
"""

CORRECTION_PROMPT = """
Correct the identified issues in the plan while maintaining its core structure.

Original Plan: {plan}
Issues to Fix: {issues}
Constraints: {constraints}

Generate a corrected version that:
1. Resolves all critical issues
2. Maintains feasibility
3. Stays aligned with constraints
4. Preserves the plan's intent

Return the corrected plan in the same JSON format as the original.
"""

class GuardrailValidator:
    """Validates outputs for hallucinations and contradictions."""
    
    def validate_plan(
        self,
        user_input: str,
        constraints: Dict[str, Any],
        plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate plan for contradictions and hallucinations.
        
        Args:
            user_input: Original user input
            constraints: Extracted constraints
            plan: Generated plan
            
        Returns:
            Validation results
        """
        prompt = VALIDATION_PROMPT.format(
            user_input=user_input,
            constraints=json.dumps(constraints, indent=2),
            plan=json.dumps(plan, indent=2)
        )
        
        result = llm_client.generate_json(
            system_prompt=SYSTEM_ROLE,
            user_prompt=prompt,
            temperature=0.3  # Lower temp for more consistent validation
        )
        
        result.setdefault("is_valid", True)
        result.setdefault("confidence", 1.0)
        result.setdefault("issues", [])
        result.setdefault("critical_issues_count", 0)
        result.setdefault("recommendation", "approve")
        
        return result
    
    def correct_plan(
        self,
        plan: Dict[str, Any],
        issues: List[Dict[str, Any]],
        constraints: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Automatically correct issues in the plan.
        
        Args:
            plan: Original plan
            issues: Identified issues
            constraints: User constraints
            
        Returns:
            Corrected plan
        """
        # Only correct if there are issues
        if not issues:
            return plan
        
        prompt = CORRECTION_PROMPT.format(
            plan=json.dumps(plan, indent=2),
            issues=json.dumps(issues, indent=2),
            constraints=json.dumps(constraints, indent=2)
        )
        
        corrected = llm_client.generate_json(
            system_prompt=SYSTEM_ROLE,
            user_prompt=prompt,
            temperature=0.5
        )
        
        return corrected
    
    def validate_and_correct(
        self,
        user_input: str,
        constraints: Dict[str, Any],
        plan: Dict[str, Any],
        auto_correct: bool = True
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Validate plan and optionally auto-correct issues.
        
        Args:
            user_input: Original input
            constraints: Constraints
            plan: Generated plan
            auto_correct: Whether to auto-correct issues
            
        Returns:
            Tuple of (validation_results, corrected_plan)
        """
        validation = self.validate_plan(user_input, constraints, plan)
        
        corrected_plan = plan
        
        if not validation.get("is_valid") and auto_correct:
            critical_issues = [
                issue for issue in validation.get("issues", [])
                if issue.get("severity") in ["critical", "high"]
            ]
            
            if critical_issues:
                corrected_plan = self.correct_plan(plan, critical_issues, constraints)
                validation["was_corrected"] = True
                validation["corrections_applied"] = len(critical_issues)
        
        return validation, corrected_plan
    
    def check_constraint_violations(
        self,
        plan: Dict[str, Any],
        constraints: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Check for specific constraint violations.
        
        Args:
            plan: Generated plan
            constraints: User constraints
            
        Returns:
            List of violations
        """
        violations = []
        
        # Check time constraint
        time_constraint = constraints.get("time_constraint", {})
        if time_constraint.get("value"):
            # Simple heuristic check
            plan_time = plan.get("total_estimated_time", "")
            if "month" in plan_time.lower() and "week" in time_constraint.get("value", "").lower():
                violations.append({
                    "type": "time_violation",
                    "severity": "high",
                    "description": f"Plan requires {plan_time} but constraint is {time_constraint['value']}"
                })
        
        # Check budget constraint
        resources = constraints.get("resources", {})
        budget = resources.get("budget")
        if budget:
            plan_cost = plan.get("total_cost", "")
            # Add budget validation logic here
        
        return violations

guardrail_validator = GuardrailValidator()
