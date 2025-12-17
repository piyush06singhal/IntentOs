"""Configuration and environment settings for IntentOS."""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings loaded from environment variables."""
    
    def __init__(self):
        """Initialize settings from environment or Streamlit secrets."""
        # Try to import streamlit for secrets (only available when running in Streamlit)
        try:
            import streamlit as st
            if hasattr(st, 'secrets') and len(st.secrets) > 0:
                # Running in Streamlit Cloud with secrets
                self.OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", "")
                self.MODEL_NAME = st.secrets.get("MODEL_NAME", "gpt-4o-mini")
                self.TEMPERATURE = float(st.secrets.get("TEMPERATURE", "0.7"))
                self.MAX_TOKENS = int(st.secrets.get("MAX_TOKENS", "2000"))
            else:
                # Running locally with .env
                self._load_from_env()
        except (ImportError, AttributeError):
            # Streamlit not available, use environment variables
            self._load_from_env()
        
        # Application Settings
        self.MAX_CLARIFICATION_QUESTIONS = 3
        self.MIN_CONFIDENCE_THRESHOLD = 0.6
        
        # UI Settings
        self.APP_TITLE = "IntentOS"
        self.APP_SUBTITLE = "AI Decision Intelligence System"
    
    def _load_from_env(self):
        """Load settings from environment variables."""
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        self.MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
        self.TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
        self.MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))
    
    def validate(self):
        """Validate required settings."""
        if not self.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is required. "
                "Please set it in .env file (local) or Streamlit secrets (cloud)."
            )
        return True

settings = Settings()
