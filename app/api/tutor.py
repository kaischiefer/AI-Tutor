from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.markdown_renderer import render_markdown
from app.services.tutor import (
    ALLOWED_DIFFICULTIES,
    TutorService,
    TutorServiceError,
)


def create_tutor_router(
    *,
    tutor_service: TutorService,
    templates: Jinja2Templates,
) -> APIRouter:
    router = APIRouter()

    @router.get("/", response_class=HTMLResponse)
    async def home(request: Request):
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "lesson": None,
                "error": None,
                "topic": "",
                "difficulty": "intermediate",
            },
        )

    @router.post("/teach", response_class=HTMLResponse)
    async def teach(
        request: Request,
        topic: str = Form(...),
        difficulty: str = Form("intermediate"),
    ):
        cleaned_topic = topic.strip()

        if difficulty not in ALLOWED_DIFFICULTIES:
            difficulty = "intermediate"

        if not cleaned_topic:
            return templates.TemplateResponse(
                request=request,
                name="index.html",
                context={
                    "lesson": None,
                    "error": "Please enter a topic.",
                    "topic": topic,
                    "difficulty": difficulty,
                },
                status_code=400,
            )

        try:
            lesson_markdown = tutor_service.generate_lesson(
                topic=cleaned_topic,
                difficulty=difficulty,
            )

            lesson_html = render_markdown(lesson_markdown)
            error = None

        except TutorServiceError:
            lesson_html = None
            error = (
                "The tutor could not generate the lesson. "
                "Review the application logs and try again."
            )

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "lesson": lesson_html,
                "error": error,
                "topic": cleaned_topic,
                "difficulty": difficulty,
            },
        )

    return router