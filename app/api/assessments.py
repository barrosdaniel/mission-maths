"""Assessments router — level checks, zone tests (asteroid fields), and placement."""
from fastapi import APIRouter

router = APIRouter(prefix="/assessments", tags=["assessments"])


@router.get("/")
async def list_assessments() -> dict:
    """Placeholder: list assessments for the current learner."""
    return {"detail": "not implemented"}
