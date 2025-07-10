"""
Google Gemini provider implementation.
"""
import os
from typing import Dict, Any, List
from .base import BaseProvider

class GeminiProvider(BaseProvider):
    """Google Gemini API provider."""
    
    def __init__(self):
        super().__init__("gemini", "gemini")
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.supported_models = [
            "gemini-2.5-pro-preview-03-25",
            "gemini-2.0-flash"
        ]
    
    def is_available(self) -> bool:
        """Check if Gemini API key is available."""
        return bool(self.api_key)
    
    def get_default_models(self) -> Dict[str, str]:
        """Get default Gemini models."""
        return {
            "big": os.getenv("BIG_MODEL", "gemini-2.5-pro-preview-03-25"),
            "small": os.getenv("SMALL_MODEL", "gemini-2.0-flash")
        }
    
    def get_supported_models(self) -> List[str]:
        """Get list of supported Gemini models."""
        return self.supported_models
    
    def configure_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Configure request for Gemini."""
        request["api_key"] = self.api_key
        
        self.logger.debug(f"Configured Gemini request for model: {request.get('model')}")
        return request