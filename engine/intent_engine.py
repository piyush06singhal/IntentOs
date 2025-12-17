"""Intent detection and extraction engine."""
from typing import Dict, Any
from utils.llm_client import llm_client
from config.prompts import SYSTEM_ROLE, INTENT_EXTRACTION_PROMPT

class IntentEngine:
    """Handles intent detection and extraction from user input."""
    
    def extract_intent(self, user_input: str) -> Dict[str, Any]:
        """
        Extract structured intent from user input.
        
        Args:
            user_input: Raw user input text
            
        Returns:
            Dictionary containing:
                - primary_intent: Main goal
                - secondary_intents: Related goals
                - confidence_score: Clarity score (0-1)
                - intent_category: Category of intent
                - reasoning: Analysis explanation
        """
        prompt = INTENT_EXTRACTION_PROMPT.format(user_input=user_input)
        
        result = llm_client.generate_json(
            system_prompt=SYSTEM_ROLE,
            user_prompt=prompt,
            temperature=0.5  # Lower temperature for more consistent extraction
        )
        
        # Validate and normalize
        result.setdefault("primary_intent", "Unknown")
        result.setdefault("secondary_intents", [])
        result.setdefault("confidence_score", 0.5)
        result.setdefault("intent_category", "general")
        result.setdefault("reasoning", "")
        
        # Ensure confidence is between 0 and 1
        result["confidence_score"] = max(0.0, min(1.0, float(result["confidence_score"])))
        
        return result

intent_engine = IntentEngine()
