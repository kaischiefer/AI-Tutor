from pathlib import Path

from app.providers.base import LLMProvider, LLMProviderError


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TEACHER_PROMPT_PATH = PROJECT_ROOT / "prompts" / "teacher.txt"

ALLOWED_DIFFICULTIES = {
    "beginner",
    "intermediate",
    "advanced",
}


class TutorServiceError(RuntimeError):
    """Raised when the tutor cannot generate a lesson."""


class TutorService:
    def __init__(self, provider: LLMProvider) -> None:
        self.provider = provider
        self.teacher_prompt = TEACHER_PROMPT_PATH.read_text(
            encoding="utf-8"
        ).strip()

    def generate_lesson(
        self,
        *,
        topic: str,
        difficulty: str,
    ) -> str:
        cleaned_topic = topic.strip()

        if not cleaned_topic:
            raise ValueError("Topic cannot be empty.")

        if difficulty not in ALLOWED_DIFFICULTIES:
            raise ValueError(
                f"Unsupported difficulty: {difficulty}"
            )

        user_prompt = f"""
Topic: {cleaned_topic}
Difficulty: {difficulty}

Generate a complete lesson for this topic.
""".strip()

        try:
            return self.provider.generate(
                system_prompt=self.teacher_prompt,
                user_prompt=user_prompt,
            )
        except LLMProviderError as exc:
            raise TutorServiceError(
                "The tutor could not generate the lesson."
            ) from exc