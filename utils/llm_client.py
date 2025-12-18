"""LLM client abstraction layer for easy model swapping."""
import json
from typing import Dict, Any, Optional
from config.settings import settings

class LLMClient:
    """Abstraction layer for LLM interactions."""
    
    def __init__(self):
        """Initialize the LLM client."""
        self.provider = settings.LLM_PROVIDER
        self.model = settings.MODEL_NAME
        self.temperature = settings.TEMPERATURE
        self.max_tokens = settings.MAX_TOKENS
        
        if self.provider == "openai":
            from openai import OpenAI
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        elif self.provider == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.client = genai.GenerativeModel(self.model)
        elif self.provider == "ollama":
            # Ollama runs locally - no API key needed!
            try:
                import requests
                self.client = None  # We'll use requests directly
                self.ollama_url = settings.OLLAMA_URL
            except ImportError:
                raise ImportError("requests library required for Ollama")
    
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        response_format: Optional[str] = None
    ) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            system_prompt: System role and instructions
            user_prompt: User message
            temperature: Override default temperature
            max_tokens: Override default max tokens
            response_format: Optional response format ("json_object" for JSON mode)
            
        Returns:
            Generated text response
        """
        if self.provider == "openai":
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            kwargs = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature or self.temperature,
                "max_tokens": max_tokens or self.max_tokens
            }
            
            if response_format == "json_object":
                kwargs["response_format"] = {"type": "json_object"}
            
            response = self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
        
        elif self.provider == "gemini":
            # Combine system and user prompts for Gemini
            combined_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            if response_format == "json_object":
                combined_prompt += "\n\nIMPORTANT: Return ONLY valid JSON, no additional text."
            
            generation_config = {
                "temperature": temperature or self.temperature,
                "max_output_tokens": max_tokens or self.max_tokens,
            }
            
            response = self.client.generate_content(
                combined_prompt,
                generation_config=generation_config
            )
            return response.text
        
        elif self.provider == "ollama":
            # Ollama - local LLM, no rate limits!
            import requests
            
            combined_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            if response_format == "json_object":
                combined_prompt += "\n\nIMPORTANT: Return ONLY valid JSON, no additional text."
            
            payload = {
                "model": self.model,
                "prompt": combined_prompt,
                "stream": False,
                "options": {
                    "temperature": temperature or self.temperature,
                    "num_predict": max_tokens or self.max_tokens
                }
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                raise Exception(f"Ollama error: {response.text}")
    
    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate a JSON response from the LLM.
        
        Args:
            system_prompt: System role and instructions
            user_prompt: User message (should request JSON output)
            temperature: Override default temperature
            max_tokens: Override default max tokens
            
        Returns:
            Parsed JSON object
        """
        response_text = self.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format="json_object"
        )
        
        try:
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            # Fallback: try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            raise ValueError(f"Failed to parse JSON response: {e}")

# Global client instance
llm_client = LLMClient()
