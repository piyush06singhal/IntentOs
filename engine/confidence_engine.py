"""Confidence-Driven Clarification Engine."""
import json
from typing import Dict, Any, List
from utils.llm_client import llm_client
from config.prompts import SYSTEM_ROLE

CONFIDENCE_ASSESSMENT_PROMPT = """
Assess the confidence level for each aspect of the extracted intent and constraints.

User Input: {user_input}
Intent Data: {intent_data}
Constraint Data: {constraint_data}

For each key aspect, provide:
1. Confidence score (0.0-1.0)
2. Reason for the score
3. What information would increase confidence

Return JSON:
{{
    "overall_confidence": 0.0-1.0,
    "aspect_scores": {{
        "primary_goal": {{"score": 0.0-1.0, "reason": "why"}},
        "timeline": {{"score": 0.0-1.0, "reason": "why"}},
        "resources": {{"score": 0.0-1.0, "reason": "why"}},
        "constraints": {{"score": 0.0-1.0, "reason": "why"}},
        "success_criteria": {{"score": 0.0-1.0, "reason": "why"}}
    }},
    "low_confidence_areas": ["list of areas needing clarification"],
    "critical_gaps": ["must-have information that's missing"],
    "nice_to_have_gaps": ["optional information that would help"]
}}
"""

SMART_QUESTION_GENERATION_PROMPT = """
Generate the MINIMUM number of high-value questions to resolve low-confidence areas.

Low Confidence Areas: {low_confidence_areas}
Critical Gaps: {critical_gaps}
User Input: {user_input}

Rules:
1. Only ask about critical gaps if confidence < {threshold}
2. Combine related questions
3. Make questions specific and actionable
4. Prioritize by impact on plan quality

Return JSON:
{{
    "should_ask_questions": boolean,
    "questions": [
        {{
            "question": "specific question",
            "reason": "why this matters",
            "impact_score": 0.0-1.0,
            "category": "goal/timeline/resources/constraints",
            "is_critical": boolean
        }}
    ],
    "estimated_confidence_gain": 0.0-1.0
}}
"""

class ConfidenceEngine:
    """Manages confidence-driven clarification process."""
    
    def __init__(self, min_confidence_threshold: float = 0.6):
        """Initialize with confidence threshold."""
        self.min_confidence_threshold = min_confidence_threshold
    
    def assess_confidence(
        self,
        user_input: str,
        intent_data: Dict[str, Any],
        constraint_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Assess confidence in extracted information.
        
        Args:
            user_input: Original input
            intent_data: Extracted intent
            constraint_data: Extracted constraints
            
        Returns:
            Confidence assessment
        """
        prompt = CONFIDENCE_ASSESSMENT_PROMPT.format(
            user_input=user_input,
            intent_data=json.dumps(intent_data, indent=2),
            constraint_data=json.dumps(constraint_data, indent=2)
        )
        
        result = llm_client.generate_json(
            system_prompt=SYSTEM_ROLE,
            user_prompt=prompt,
            temperature=0.5
        )
        
        result.setdefault("overall_confidence", 0.5)
        result.setdefault("aspect_scores", {})
        result.setdefault("low_confidence_areas", [])
        result.setdefault("critical_gaps", [])
        result.setdefault("nice_to_have_gaps", [])
        
        return result
    
    def generate_smart_questions(
        self,
        confidence_assessment: Dict[str, Any],
        user_input: str,
        max_questions: int = 3
    ) -> Dict[str, Any]:
        """
        Generate minimal, high-impact clarification questions.
        
        Args:
            confidence_assessment: Confidence assessment results
            user_input: Original input
            max_questions: Maximum questions to ask
            
        Returns:
            Smart questions
        """
        prompt = SMART_QUESTION_GENERATION_PROMPT.format(
            low_confidence_areas=json.dumps(confidence_assessment.get("low_confidence_areas", [])),
            critical_gaps=json.dumps(confidence_assessment.get("critical_gaps", [])),
            user_input=user_input,
            threshold=self.min_confidence_threshold
        )
        
        result = llm_client.generate_json(
            system_prompt=SYSTEM_ROLE,
            user_prompt=prompt,
            temperature=0.7
        )
        
        result.setdefault("should_ask_questions", False)
        result.setdefault("questions", [])
        result.setdefault("estimated_confidence_gain", 0.0)
        
        # Limit questions
        if len(result["questions"]) > max_questions:
            # Sort by impact and keep top N
            result["questions"].sort(key=lambda q: q.get("impact_score", 0), reverse=True)
            result["questions"] = result["questions"][:max_questions]
        
        return result
    
    def should_ask_clarifications(self, confidence_assessment: Dict[str, Any]) -> bool:
        """
        Determine if clarification questions are needed.
        
        Args:
            confidence_assessment: Confidence assessment
            
        Returns:
            True if questions needed
        """
        overall = confidence_assessment.get("overall_confidence", 1.0)
        has_critical_gaps = len(confidence_assessment.get("critical_gaps", [])) > 0
        
        return overall < self.min_confidence_threshold or has_critical_gaps
    
    def update_confidence_with_answers(
        self,
        original_confidence: Dict[str, Any],
        answers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Update confidence scores after receiving answers.
        
        Args:
            original_confidence: Original assessment
            answers: User answers to questions
            
        Returns:
            Updated confidence assessment
        """
        # Simple heuristic: each answer increases confidence
        boost_per_answer = 0.15
        num_answers = len([a for a in answers.values() if a.strip()])
        
        new_confidence = min(1.0, original_confidence.get("overall_confidence", 0.5) + 
                            (num_answers * boost_per_answer))
        
        updated = original_confidence.copy()
        updated["overall_confidence"] = new_confidence
        updated["answers_provided"] = num_answers
        
        return updated

confidence_engine = ConfidenceEngine()
