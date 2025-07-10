"""
OpenAI provider implementation.
"""
import os
from typing import Dict, Any, List
from .base import BaseProvider

class OpenAIProvider(BaseProvider):
    """OpenAI API provider."""
    
    def __init__(self):
        super().__init__("openai", "openai")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.supported_models = [
            "o3-mini",
            "o1",
            "o1-mini", 
            "o1-pro",
            "gpt-4.5-preview",
            "gpt-4o",
            "gpt-4o-audio-preview", 
            "chatgpt-4o-latest",
            "gpt-4o-mini",
            "gpt-4o-mini-audio-preview",
            "gpt-4.1",
            "gpt-4.1-mini"
        ]
    
    def is_available(self) -> bool:
        """Check if OpenAI API key is available."""
        return bool(self.api_key)
    
    def get_default_models(self) -> Dict[str, str]:
        """Get default OpenAI models."""
        return {
            "big": os.getenv("BIG_MODEL", "gpt-4.1"),
            "small": os.getenv("SMALL_MODEL", "gpt-4.1-mini")
        }
    
    def get_supported_models(self) -> List[str]:
        """Get list of supported OpenAI models."""
        return self.supported_models
    
    def configure_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Configure request for OpenAI."""
        request["api_key"] = self.api_key
        
        self.logger.debug(f"Configured OpenAI request for model: {request.get('model')}")
        return request