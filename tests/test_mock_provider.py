from app.providers.mock_provider import MockProvider


def test_mock_provider_returns_lesson() -> None:
    provider = MockProvider()

    response = provider.generate(
        system_prompt="You are a tutor.",
        user_prompt="Teach gradient descent.",
    )

    assert response
    assert "Mock Lesson" in response