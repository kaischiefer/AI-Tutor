from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.tutor import create_tutor_router
from app.config import get_settings
from app.providers.factory import create_llm_provider
from app.services.tutor import TutorService


APP_DIR = Path(__file__).resolve().parent

settings = get_settings()
provider = create_llm_provider(settings)
tutor_service = TutorService(provider=provider)

templates = Jinja2Templates(
    directory=APP_DIR / "templates"
)

app = FastAPI(
    title="AI Knowledge Tutor",
    version="0.1.0",
)

app.mount(
    "/static",
    StaticFiles(directory=APP_DIR / "static"),
    name="static",
)

app.include_router(
    create_tutor_router(
        tutor_service=tutor_service,
        templates=templates,
    )
)