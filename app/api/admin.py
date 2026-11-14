"""Admin router — platform administration: accounts, curriculum management, support."""
from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/")
async def admin_index() -> dict:
    """Placeholder: admin index."""
    return {"detail": "not implemented"}
