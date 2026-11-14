"""Curriculum router — read-only access to curriculum data (levels, waypoints, thresholds)."""
from fastapi import APIRouter

router = APIRouter(prefix="/curriculum", tags=["curriculum"])


@router.get("/levels")
async def list_levels() -> dict:
    """Placeholder: return all curriculum levels."""
    return {"detail": "not implemented"}
