from abc import ABC, abstractmethod


class LLMProviderError(RuntimeError):
    """Raised when an LLM provider cannot complete a request."""


class LLMProvider(ABC):
    """Interface implemented by all language-model providers."""

    @abstractmethod
    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        """Generate text from the supplied prompts."""