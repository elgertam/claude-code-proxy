"""
Provider registry for managing AI model providers.
"""
import logging
from typing import Dict, List, Optional, Tuple
from .base import BaseProvider
from .openai import OpenAIProvider
from .gemini import GeminiProvider
from .azure import AzureOpenAIProvider
from .anthropic import AnthropicProvider

class ProviderRegistry:
    """Registry for managing AI model providers."""
    
    def __init__(self):
        self.providers: Dict[str, BaseProvider] = {}
        self.logger = logging.getLogger("providers.registry")
        self._register_default_providers()
    
    def _register_default_providers(self):
        """Register all default providers."""
        default_providers = [
            OpenAIProvider(),
            GeminiProvider(),
            AzureOpenAIProvider(),
            AnthropicProvider()
        ]
        
        for provider in default_providers:
            self.register_provider(provider)
    
    def register_provider(self, provider: BaseProvider):
        """Register a new provider."""
        self.providers[provider.name] = provider
        self.logger.debug(f"Registered provider: {provider.name}")
    
    def get_provider(self, name: str) -> Optional[BaseProvider]:
        """Get a provider by name."""
        return self.providers.get(name)
    
    def get_preferred_provider(self) -> Optional[BaseProvider]:
        """Get the preferred provider."""
        import os
        preferred = os.getenv("PREFERRED_PROVIDER", "openai").lower()
        return self.get_provider(preferred)
    
    def get_available_providers(self) -> List[BaseProvider]:
        """Get all available providers (those with valid credentials)."""
        return [provider for provider in self.providers.values() if provider.is_available()]
    
    def get_provider_by_model(self, model: str) -> Optional[BaseProvider]:
        """Get the provider for a specific model based on prefix."""
        if "/" in model:
            prefix = model.split("/")[0]
            for provider in self.providers.values():
                if provider.prefix == prefix:
                    return provider
        return None
    
    def map_model(self, model: str) -> tuple[str, BaseProvider]:
        """
        Map a model name to a provider and return the mapped model and provider.
        
        Returns:
            tuple: (mapped_model, provider)
        """
        # Check if model has a provider prefix
        provider = self.get_provider_by_model(model)
        if provider:
            return model, provider
        
        # Map common model names to providers
        if model.lower() in ["sonnet", "haiku"]:
            preferred = self.get_preferred_provider()
            if preferred and preferred.is_available():
                model_type = "big" if model.lower() == "sonnet" else "small"
                mapped_model = preferred.map_model(model, model_type)
                return mapped_model, preferred
        
        # Default to first available provider
        available = self.get_available_providers()
        if available:
            provider = available[0]
            return provider.map_model(model), provider
        
        # No available providers
        self.logger.error("No available providers found")
        return model, None
    
    def get_all_supported_models(self) -> Dict[str, List[str]]:
        """Get all supported models grouped by provider."""
        return {
            name: provider.get_supported_models() 
            for name, provider in self.providers.items()
        }
    
    def get_provider_names(self) -> List[str]:
        """Get all registered provider names."""
        return list(self.providers.keys())
    
    def get_available_provider_names(self) -> List[str]:
        """Get names of available providers."""
        return [provider.name for provider in self.get_available_providers()]

# Global registry instance
registry = ProviderRegistry()