"""Persistent Intent Memory with Drift Detection."""
import json
import os
from datetime import datetime
from typing import Dict, Any, List
from utils.llm_client import llm_client
from config.prompts import SYSTEM_ROLE

DRIFT_DETECTION_PROMPT = """
Compare the user's current intent with their historical intents to detect changes.

Current Intent: {current_intent}
Historical Intents: {historical_intents}

Analyze:
1. Has the core goal changed?
2. Have priorities shifted?
3. Are constraints different?
4. Is this a natural evolution or a pivot?

Return JSON:
{{
    "has_drifted": boolean,
    "drift_type": "none/evolution/pivot/expansion/abandonment",
    "drift_severity": 0.0-1.0,
    "changes_detected": [
        {{
            "aspect": "goal/priority/constraint/approach",
            "old_value": "previous",
            "new_value": "current",
            "significance": "high/medium/low"
        }}
    ],
    "recommendation": "continue/adapt/restart/clarify",
    "reasoning": "why this recommendation"
}}
"""

class IntentMemory:
    """Manages persistent intent memory and drift detection."""
    
    def __init__(self, memory_dir: str = "intent_memory"):
        """Initialize intent memory system."""
        self.memory_dir = memory_dir
        os.makedirs(memory_dir, exist_ok=True)
    
    def _get_user_memory_file(self, user_id: str = "default") -> str:
        """Get path to user's memory file."""
        return os.path.join(self.memory_dir, f"{user_id}_memory.json")
    
    def save_intent(
        self,
        intent_data: Dict[str, Any],
        constraint_data: Dict[str, Any],
        plan_data: Dict[str, Any],
        user_id: str = "default"
    ) -> None:
        """Save intent to persistent memory."""
        memory_file = self._get_user_memory_file(user_id)
        memory = self._load_memory(user_id)
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "intent": intent_data,
            "constraints": constraint_data,
            "plan": plan_data,
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S")
        }
        
        memory["intents"].append(entry)
        memory["last_updated"] = datetime.now().isoformat()
        memory["total_sessions"] = len(memory["intents"])
        
        with open(memory_file, 'w', encoding='utf-8') as f:
            json.dump(memory, f, indent=2, ensure_ascii=False)
    
    def _load_memory(self, user_id: str = "default") -> Dict[str, Any]:
        """Load user's intent memory."""
        memory_file = self._get_user_memory_file(user_id)
        
        if os.path.exists(memory_file):
            with open(memory_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return {
            "user_id": user_id,
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "intents": [],
            "total_sessions": 0
        }
    
    def get_intent_history(self, user_id: str = "default", limit: int = 10) -> List[Dict[str, Any]]:
        """Get user's intent history."""
        memory = self._load_memory(user_id)
        intents = memory.get("intents", [])
        return list(reversed(intents[-limit:]))
    
    def detect_drift(self, current_intent: Dict[str, Any], user_id: str = "default") -> Dict[str, Any]:
        """Detect if user's intent has drifted from previous sessions."""
        history = self.get_intent_history(user_id, limit=5)
        
        if not history:
            return {
                "has_drifted": False,
                "drift_type": "none",
                "drift_severity": 0.0,
                "changes_detected": [],
                "recommendation": "continue",
                "reasoning": "No historical data available"
            }
        
        prompt = DRIFT_DETECTION_PROMPT.format(
            current_intent=json.dumps(current_intent, indent=2),
            historical_intents=json.dumps([h.get("intent", {}) for h in history], indent=2)
        )
        
        result = llm_client.generate_json(
            system_prompt=SYSTEM_ROLE,
            user_prompt=prompt,
            temperature=0.6
        )
        
        result.setdefault("has_drifted", False)
        result.setdefault("drift_type", "none")
        result.setdefault("drift_severity", 0.0)
        result.setdefault("changes_detected", [])
        result.setdefault("recommendation", "continue")
        result.setdefault("reasoning", "")
        
        return result

intent_memory = IntentMemory()
