"""
Anthropic provider implementation.
"""
import os
from typing import Dict, Any, List
from .base import BaseProvider

class AnthropicProvider(BaseProvider):
    """Anthropic API provider."""
    
    def __init__(self):
        super().__init__("anthropic", "anthropic")
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.supported_models = [
            "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022",
            "claude-3-opus-20240229"
        ]
    
    def is_available(self) -> bool:
        """Check if Anthropic API key is available."""
        return bool(self.api_key)
    
    def get_default_models(self) -> Dict[str, str]:
        """Get default Anthropic models."""
        return {
            "big": os.getenv("BIG_MODEL", "claude-3-5-sonnet-20241022"),
            "small": os.getenv("SMALL_MODEL", "claude-3-5-haiku-20241022")
        }
    
    def get_supported_models(self) -> List[str]:
        """Get list of supported Anthropic models."""
        return self.supported_models
    
    def configure_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Configure request for Anthropic."""
        request["api_key"] = self.api_key
        
        self.logger.debug(f"Configured Anthropic request for model: {request.get('model')}")
        return request