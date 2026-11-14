"""Mission Maths — application entry point.

Initialises the FastAPI app, mounts all domain routers, and starts NiceGUI
as the application shell serving all learner-facing and parent-facing pages.

Usage:
    poetry run uvicorn app.main:fastapi_app --reload
"""
from fastapi import FastAPI
from nicegui import ui

from app.api import admin, assessments, curriculum, parent, progress, sessions
from app.config import settings
from web.pages import landing

# ── FastAPI app ──────────────────────────────────────────────────────────────
fastapi_app = FastAPI(
    title="Mission Maths",
    description="A mastery-based maths fluency platform for children.",
    version="0.1.0",
)

fastapi_app.include_router(sessions.router)
fastapi_app.include_router(assessments.router)
fastapi_app.include_router(progress.router)
fastapi_app.include_router(curriculum.router)
fastapi_app.include_router(parent.router)
fastapi_app.include_router(admin.router)


@fastapi_app.get("/health")
async def health() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}


# ── NiceGUI pages ────────────────────────────────────────────────────────────
landing.create()

# ── Mount NiceGUI into the FastAPI app ───────────────────────────────────────
ui.run_with(
    fastapi_app,
    title="Mission Maths",
    favicon="🚀",
    dark=True,
    storage_secret=settings.secret_key,
)
