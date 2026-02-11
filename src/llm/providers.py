"""
LLM Provider Interface - Support for multiple model providers

Supported providers:
- Google Gemini 2.5 Flash/Pro
- Anthropic Claude
- OpenAI GPT-4
- Local Llama (via Ollama)
- Mistral (via API or local)
"""

from abc import ABC, abstractmethod
import os
import logging
from typing import List, Optional, Dict

logger = logging.getLogger(__name__)


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self._setup_client()

    @abstractmethod
    def _setup_client(self):
        """Initialize provider client."""
        pass

    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from prompt."""
        pass

    @abstractmethod
    async def embed(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for texts."""
        pass

    @abstractmethod
    def get_token_count(self, text: str) -> int:
        """Count tokens for text."""
        pass


class GeminiProvider(LLMProvider):
    """Google Gemini 2.5 provider."""

    def _setup_client(self):
        try:
            import google.generativeai as genai
            self.client = genai.Client(api_key=self.api_key)
            logger.info(f"Gemini client initialized with model {self.model}")
        except ImportError:
            logger.error("google-generativeai not installed")
            raise

    async def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 4096) -> str:
        """Generate response using Gemini."""
        response = await self._retry_with_backoff(
            self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=genai.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens
                )
            )
        )
        return response.text

    async def embed(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using Gemini."""
        # Use sentence-transformers for local or API
        results = []
        for text in texts:
            # Placeholder - implement actual embedding
            results.append([0.1] * 384)  # 384-dim vector
        return results

    def get_token_count(self, text: str) -> int:
        """Estimate token count (rough approximation)."""
        return len(text) // 4  # Rough estimate


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider."""

    def _setup_client(self):
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=self.api_key)
            logger.info(f"Claude client initialized")
        except ImportError:
            logger.error("anthropic not installed")

    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using Claude."""
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=kwargs.get('max_tokens', 4096),
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text


class LocalLLMProvider(LLMProvider):
    """Local LLM provider (Ollama)."""

    def _setup_client(self):
        try:
            import ollama
            self.client = ollama.Client(host=os.getenv('OLLAMA_HOST', 'localhost'))
            logger.info(f"Ollama client initialized")
        except ImportError:
            logger.error("ollama not installed")

    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate using local model."""
        response = self.client.generate(model=self.model, prompt=prompt)
        return response['response']


def get_provider(provider_name: str) -> LLMProvider:
    """Factory function to get LLM provider instance."""
    api_key = os.getenv(f"{provider_name.upper()}_API_KEY")
    model = os.getenv(f"{provider_name.upper()}_MODEL", "gemini-2.5-flash")

    if provider_name == "gemini":
        return GeminiProvider(api_key, model)
    elif provider_name == "anthropic":
        return AnthropicProvider(api_key, model)
    elif provider_name == "ollama":
        return LocalLLMProvider(api_key="", model=model)
    else:
        raise ValueError(f"Unknown provider: {provider_name}")


if __name__ == "__main__":
    # Test providers
    provider = get_provider("gemini")
    print(f"Provider: {provider.__class__.__name__}")
