"""
Azure OpenAI provider implementation.
"""
import os
from typing import Dict, Any, List
from .base import BaseProvider

class AzureOpenAIProvider(BaseProvider):
    """Azure OpenAI API provider."""
    
    def __init__(self):
        super().__init__("azure", "azure")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")
        self.supported_models = [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4",
            "gpt-35-turbo"
        ]
    
    def is_available(self) -> bool:
        """Check if Azure OpenAI configuration is available."""
        return bool(self.api_key and self.endpoint)
    
    def get_default_models(self) -> Dict[str, str]:
        """Get default Azure OpenAI models (deployment names)."""
        return {
            "big": os.getenv("BIG_MODEL", "gpt-4o"),
            "small": os.getenv("SMALL_MODEL", "gpt-4o-mini")
        }
    
    def get_supported_models(self) -> List[str]:
        """Get list of supported Azure OpenAI models."""
        return self.supported_models
    
    def configure_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Configure request for Azure OpenAI."""
        request["api_key"] = self.api_key
        request["api_base"] = self.endpoint
        request["api_version"] = self.api_version
        
        self.logger.debug(f"Configured Azure OpenAI request for model: {request.get('model')}")
        return request