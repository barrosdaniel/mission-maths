"""Progress router — learner progress, mastery state, and fluency trends."""
from fastapi import APIRouter

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("/{learner_id}")
async def get_progress(learner_id: int) -> dict:
    """Placeholder: return progress summary for a learner."""
    return {"detail": "not implemented"}
