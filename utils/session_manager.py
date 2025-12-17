"""Session management utilities for saving and loading analysis sessions."""
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

class SessionManager:
    """Manages saving and loading of analysis sessions."""
    
    def __init__(self, sessions_dir: str = "sessions"):
        """Initialize session manager."""
        self.sessions_dir = sessions_dir
        os.makedirs(sessions_dir, exist_ok=True)
    
    def save_session(
        self,
        intent_data: Dict[str, Any],
        constraint_data: Dict[str, Any],
        plan_data: Dict[str, Any],
        user_input: str,
        alternatives: List[Dict[str, Any]] = None,
        session_name: Optional[str] = None
    ) -> str:
        """
        Save a session to disk.
        
        Args:
            intent_data: Intent analysis data
            constraint_data: Constraint analysis data
            plan_data: Action plan data
            user_input: Original user input
            alternatives: Alternative strategies
            session_name: Optional custom session name
            
        Returns:
            Path to saved session file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if session_name:
            filename = f"{session_name}_{timestamp}.json"
        else:
            filename = f"session_{timestamp}.json"
        
        filepath = os.path.join(self.sessions_dir, filename)
        
        session_data = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "intent": intent_data,
            "constraints": constraint_data,
            "plan": plan_data,
            "alternatives": alternatives or [],
            "metadata": {
                "app": "IntentOS",
                "version": "2.0"
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def load_session(self, filename: str) -> Dict[str, Any]:
        """
        Load a session from disk.
        
        Args:
            filename: Name of session file
            
        Returns:
            Session data dictionary
        """
        filepath = os.path.join(self.sessions_dir, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_sessions(self) -> List[Dict[str, str]]:
        """
        List all saved sessions.
        
        Returns:
            List of session info dictionaries
        """
        sessions = []
        
        if not os.path.exists(self.sessions_dir):
            return sessions
        
        for filename in os.listdir(self.sessions_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.sessions_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    sessions.append({
                        "filename": filename,
                        "timestamp": data.get("timestamp", "Unknown"),
                        "user_input": data.get("user_input", "")[:100],
                        "filepath": filepath
                    })
                except Exception:
                    continue
        
        # Sort by timestamp (newest first)
        sessions.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return sessions
    
    def delete_session(self, filename: str) -> bool:
        """
        Delete a saved session.
        
        Args:
            filename: Name of session file
            
        Returns:
            True if successful
        """
        filepath = os.path.join(self.sessions_dir, filename)
        
        try:
            os.remove(filepath)
            return True
        except Exception:
            return False

# Global instance
session_manager = SessionManager()
