"""Mission Maths — application entry point.

Initialises the FastAPI app, mounts all domain routers, and configures middleware.
"""
from fastapi import FastAPI

from app.api import admin, assessments, curriculum, parent, progress, sessions

app = FastAPI(
    title="Mission Maths",
    description="A mastery-based maths fluency platform for children.",
    version="0.1.0",
)

app.include_router(sessions.router)
app.include_router(assessments.router)
app.include_router(progress.router)
app.include_router(curriculum.router)
app.include_router(parent.router)
app.include_router(admin.router)


@app.get("/health")
async def health() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}
