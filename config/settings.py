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
                self.LLM_PROVIDER = st.secrets.get("LLM_PROVIDER", "gemini")
                self.OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", "")
                self.GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
                self.MODEL_NAME = st.secrets.get("MODEL_NAME", "gemini-2.5-flash")
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
        self.LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
        self.MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")
        self.TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
        self.MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))
    
    def validate(self):
        """Validate required settings."""
        if self.LLM_PROVIDER == "openai" and not self.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is required when using OpenAI. "
                "Please set it in .env file (local) or Streamlit secrets (cloud)."
            )
        elif self.LLM_PROVIDER == "gemini" and not self.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is required when using Gemini. "
                "Get your free key at: https://makersuite.google.com/app/apikey"
            )
        return True

settings = Settings()
