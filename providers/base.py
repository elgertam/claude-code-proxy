"""
Base provider interface for AI model providers.
"""
import os
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseProvider(ABC):
    """Base class for AI model providers."""
    
    def __init__(self, name: str, prefix: str):
        self.name = name
        self.prefix = prefix
        self.logger = logging.getLogger(f"providers.{name}")
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if this provider is available (has required API keys, etc.)."""
        pass
    
    @abstractmethod
    def get_default_models(self) -> Dict[str, str]:
        """Get default big and small models for this provider."""
        pass
    
    @abstractmethod
    def get_supported_models(self) -> List[str]:
        """Get list of supported models for this provider."""
        pass
    
    @abstractmethod
    def configure_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Configure a LiteLLM request for this provider."""
        pass
    
    def map_model(self, model_name: str, model_type: str = "auto") -> str:
        """
        Map a model name to this provider's format.
        
        Args:
            model_name: The model name to map
            model_type: Either "big", "small", or "auto" for automatic detection
        
        Returns:
            The provider-prefixed model name
        """
        # Remove any existing provider prefix
        clean_model = model_name
        if "/" in clean_model:
            clean_model = clean_model.split("/")[-1]
        
        # Map model type if specified
        if model_type == "big":
            defaults = self.get_default_models()
            clean_model = defaults.get("big", clean_model)
        elif model_type == "small":
            defaults = self.get_default_models()
            clean_model = defaults.get("small", clean_model)
        
        # Return with provider prefix
        return f"{self.prefix}/{clean_model}"
    
    def __str__(self):
        return f"{self.name}Provider"
    
    def __repr__(self):
        return f"{self.name}Provider(available={self.is_available()})"