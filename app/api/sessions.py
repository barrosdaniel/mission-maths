"""Sessions router — daily drill and level check session endpoints."""
from fastapi import APIRouter

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.get("/")
async def list_sessions() -> dict:
    """Placeholder: list sessions for the current learner."""
    return {"detail": "not implemented"}
