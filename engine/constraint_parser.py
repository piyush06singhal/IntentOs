"""Constraint extraction and parsing engine."""
from typing import Dict, Any
from utils.llm_client import llm_client
from config.prompts import SYSTEM_ROLE, CONSTRAINT_EXTRACTION_PROMPT

class ConstraintParser:
    """Handles extraction of constraints and context from user input."""
    
    def extract_constraints(self, user_input: str) -> Dict[str, Any]:
        """
        Extract structured constraints from user input.
        
        Args:
            user_input: Raw user input text
            
        Returns:
            Dictionary containing:
                - time_constraint: Time-related constraints
                - skill_level: User's skill level
                - resources: Available resources
                - preferences: User preferences
                - context: Additional context
        """
        prompt = CONSTRAINT_EXTRACTION_PROMPT.format(user_input=user_input)
        
        result = llm_client.generate_json(
            system_prompt=SYSTEM_ROLE,
            user_prompt=prompt,
            temperature=0.5
        )
        
        # Normalize structure
        result.setdefault("time_constraint", {"value": None, "urgency": None})
        result.setdefault("skill_level", None)
        result.setdefault("resources", {"budget": None, "tools": [], "team_size": None})
        result.setdefault("preferences", [])
        result.setdefault("context", "")
        
        return result
    
    def get_missing_constraints(self, constraints: Dict[str, Any]) -> list:
        """
        Identify which constraints are missing.
        
        Args:
            constraints: Extracted constraints dictionary
            
        Returns:
            List of missing constraint names
        """
        missing = []
        
        if not constraints.get("time_constraint", {}).get("value"):
            missing.append("time_constraint")
        
        if not constraints.get("skill_level"):
            missing.append("skill_level")
        
        resources = constraints.get("resources", {})
        if not resources.get("budget") and not resources.get("tools"):
            missing.append("resources")
        
        return missing

constraint_parser = ConstraintParser()
