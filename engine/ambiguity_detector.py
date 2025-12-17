"""Ambiguity detection and clarification question generation."""
import json
from typing import Dict, Any, List
from utils.llm_client import llm_client
from config.prompts import (
    SYSTEM_ROLE,
    AMBIGUITY_DETECTION_PROMPT,
    CLARIFICATION_GENERATION_PROMPT
)
from config.settings import settings

class AmbiguityDetector:
    """Detects ambiguities and generates clarification questions."""
    
    def detect_ambiguity(
        self,
        user_input: str,
        intent_data: Dict[str, Any],
        constraint_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Detect ambiguities and missing information.
        
        Args:
            user_input: Raw user input
            intent_data: Extracted intent information
            constraint_data: Extracted constraints
            
        Returns:
            Dictionary containing:
                - missing_information: Critical missing details
                - ambiguous_terms: Unclear terms
                - conflicting_constraints: Potential conflicts
                - assumptions_needed: Required assumptions
                - clarity_score: Overall clarity (0-1)
        """
        prompt = AMBIGUITY_DETECTION_PROMPT.format(
            user_input=user_input,
            intent_data=json.dumps(intent_data, indent=2),
            constraint_data=json.dumps(constraint_data, indent=2)
        )
        
        result = llm_client.generate_json(
            system_prompt=SYSTEM_ROLE,
            user_prompt=prompt,
            temperature=0.6
        )
        
        # Normalize
        result.setdefault("missing_information", [])
        result.setdefault("ambiguous_terms", [])
        result.setdefault("conflicting_constraints", [])
        result.setdefault("assumptions_needed", [])
        result.setdefault("clarity_score", 0.5)
        
        result["clarity_score"] = max(0.0, min(1.0, float(result["clarity_score"])))
        
        return result
    
    def generate_clarification_questions(
        self,
        user_input: str,
        ambiguity_data: Dict[str, Any],
        max_questions: int = None
    ) -> List[Dict[str, str]]:
        """
        Generate high-value clarification questions.
        
        Args:
            user_input: Raw user input
            ambiguity_data: Detected ambiguities
            max_questions: Maximum number of questions (default from settings)
            
        Returns:
            List of question dictionaries with:
                - question: The question text
                - reason: Why it's important
                - impact: high/medium/low
        """
        if max_questions is None:
            max_questions = settings.MAX_CLARIFICATION_QUESTIONS
        
        prompt = CLARIFICATION_GENERATION_PROMPT.format(
            user_input=user_input,
            ambiguity_data=json.dumps(ambiguity_data, indent=2),
            max_questions=max_questions
        )
        
        result = llm_client.generate_json(
            system_prompt=SYSTEM_ROLE,
            user_prompt=prompt,
            temperature=0.7
        )
        
        questions = result.get("questions", [])
        
        # Sort by impact and limit
        impact_order = {"high": 0, "medium": 1, "low": 2}
        questions.sort(key=lambda q: impact_order.get(q.get("impact", "low"), 3))
        
        return questions[:max_questions]
    
    def should_ask_clarifications(self, ambiguity_data: Dict[str, Any]) -> bool:
        """
        Determine if clarification questions are needed.
        
        Args:
            ambiguity_data: Detected ambiguities
            
        Returns:
            True if clarifications are needed
        """
        clarity_score = ambiguity_data.get("clarity_score", 1.0)
        has_missing_info = len(ambiguity_data.get("missing_information", [])) > 0
        has_conflicts = len(ambiguity_data.get("conflicting_constraints", [])) > 0
        
        return (
            clarity_score < settings.MIN_CONFIDENCE_THRESHOLD or
            has_missing_info or
            has_conflicts
        )

ambiguity_detector = AmbiguityDetector()
