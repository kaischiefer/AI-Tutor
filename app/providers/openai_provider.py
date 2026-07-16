from openai import OpenAI

from app.providers.base import LLMProvider, LLMProviderError


class OpenAIProvider(LLMProvider):
    def __init__(
        self,
        *,
        api_key: str,
        model: str,
    ) -> None:
        if not api_key:
            raise ValueError("An OpenAI API key is required.")

        if not model:
            raise ValueError("An OpenAI model must be configured.")

        self.model = model
        self.client = OpenAI(api_key=api_key)

    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        try:
            response = self.client.responses.create(
                model=self.model,
                instructions=system_prompt,
                input=user_prompt,
            )
        except Exception as exc:
            raise LLMProviderError(
                "OpenAI could not complete the request."
            ) from exc

        generated_text = response.output_text.strip()

        if not generated_text:
            raise LLMProviderError(
                "OpenAI returned an empty response."
            )

        return generated_text