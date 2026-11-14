"""Parent router — parent dashboard: learner profiles, progress view, accessibility settings."""
from fastapi import APIRouter

router = APIRouter(prefix="/parent", tags=["parent"])


@router.get("/learners")
async def list_learners() -> dict:
    """Placeholder: return learner profiles for the authenticated parent."""
    return {"detail": "not implemented"}
