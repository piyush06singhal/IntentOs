"""Multi-Intent Decomposition with Conflict Resolution Engine."""
import json
from typing import Dict, Any, List, Tuple
from utils.llm_client import llm_client
from config.prompts import SYSTEM_ROLE

MULTI_INTENT_DETECTION_PROMPT = """
Analyze the following user input and detect if there are multiple distinct goals or intents.

User Input: {user_input}

Identify:
1. All distinct goals/intents (even if related)
2. Priority/importance of each intent (high/medium/low)
3. Dependencies between intents
4. Potential conflicts (time, resources, priority, logical contradictions)

Return a JSON object with:
{{
    "has_multiple_intents": boolean,
    "intents": [
        {{
            "intent": "description",
            "priority": "high/medium/low",
            "estimated_effort": "description",
            "dependencies": ["list of other intent indices this depends on"]
        }}
    ],
    "conflicts": [
        {{
            "type": "time/resource/priority/logical",
            "description": "what conflicts",
            "affected_intents": [0, 1],
            "severity": "high/medium/low"
        }}
    ],
    "total_complexity_score": 0.0-1.0
}}
"""

CONFLICT_RESOLUTION_PROMPT = """
Given these conflicting intents and constraints, propose resolution strategies.

Intents: {intents}
Conflicts: {conflicts}
Constraints: {constraints}

For each conflict, provide:
1. Resolution strategy (prioritize, sequence, merge, split, defer)
2. Rationale
3. Impact on overall goal achievement
4. Recommended order of execution

Return JSON:
{{
    "resolutions": [
        {{
            "conflict_id": 0,
            "strategy": "prioritize/sequence/merge/split/defer",
            "rationale": "why this approach",
            "execution_order": [0, 1, 2],
            "tradeoffs": "what you gain/lose",
            "confidence": 0.0-1.0
        }}
    ],
    "recommended_approach": "overall strategy description",
    "risk_level": "low/medium/high"
}}
"""

class MultiIntentResolver:
    """Handles detection and resolution of multiple conflicting intents."""
    
    def detect_multiple_intents(self, user_input: str) -> Dict[str, Any]:
        """
        Detect if user input contains multiple intents.
        
        Args:
            user_input: Raw user input
            
        Returns:
            Dictionary with detected intents and conflicts
        """
        prompt = MULTI_INTENT_DETECTION_PROMPT.format(user_input=user_input)
        
        result = llm_client.generate_json(
            system_prompt=SYSTEM_ROLE,
            user_prompt=prompt,
            temperature=0.6
        )
        
        # Normalize
        result.setdefault("has_multiple_intents", False)
        result.setdefault("intents", [])
        result.setdefault("conflicts", [])
        result.setdefault("total_complexity_score", 0.5)
        
        return result
    
    def resolve_conflicts(
        self,
        intents: List[Dict[str, Any]],
        conflicts: List[Dict[str, Any]],
        constraints: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate conflict resolution strategies.
        
        Args:
            intents: List of detected intents
            conflicts: List of conflicts
            constraints: User constraints
            
        Returns:
            Resolution strategies
        """
        prompt = CONFLICT_RESOLUTION_PROMPT.format(
            intents=json.dumps(intents, indent=2),
            conflicts=json.dumps(conflicts, indent=2),
            constraints=json.dumps(constraints, indent=2)
        )
        
        result = llm_client.generate_json(
            system_prompt=SYSTEM_ROLE,
            user_prompt=prompt,
            temperature=0.7
        )
        
        result.setdefault("resolutions", [])
        result.setdefault("recommended_approach", "")
        result.setdefault("risk_level", "medium")
        
        return result
    
    def prioritize_intents(
        self,
        intents: List[Dict[str, Any]],
        constraints: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Prioritize intents based on constraints and dependencies.
        
        Args:
            intents: List of intents
            constraints: User constraints
            
        Returns:
            Sorted list of intents by priority
        """
        # Score each intent
        scored_intents = []
        
        for i, intent in enumerate(intents):
            score = 0.0
            
            # Priority weight
            priority_weights = {"high": 1.0, "medium": 0.6, "low": 0.3}
            score += priority_weights.get(intent.get("priority", "medium"), 0.5)
            
            # Dependency penalty (dependent intents score lower)
            deps = intent.get("dependencies", [])
            score -= len(deps) * 0.1
            
            # Urgency from constraints
            if constraints.get("time_constraint", {}).get("urgency") == "high":
                score += 0.2
            
            scored_intents.append({
                "index": i,
                "intent": intent,
                "score": max(0.0, min(1.0, score))
            })
        
        # Sort by score descending
        scored_intents.sort(key=lambda x: x["score"], reverse=True)
        
        return [item["intent"] for item in scored_intents]

multi_intent_resolver = MultiIntentResolver()
