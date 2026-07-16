from app.config import Settings
from app.providers.base import LLMProvider
from app.providers.mock_provider import MockProvider
from app.providers.openai_provider import OpenAIProvider


def create_llm_provider(settings: Settings) -> LLMProvider:
    if settings.llm_provider == "openai":
        if not settings.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY must be set when "
                "LLM_PROVIDER=openai."
            )

        if not settings.openai_model:
            raise ValueError(
                "OPENAI_MODEL must be set when "
                "LLM_PROVIDER=openai."
            )

        return OpenAIProvider(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
        )

    if settings.llm_provider == "mock":
        return MockProvider()

    if settings.llm_provider == "ollama":
        raise NotImplementedError(
            "The Ollama provider has not been implemented yet."
        )

    raise ValueError(
        f"Unsupported LLM provider: {settings.llm_provider}"
    )