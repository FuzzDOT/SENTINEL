from fastapi import APIRouter

router = APIRouter(prefix="/admin")


@router.get("/stats")
def admin_stats():
    return {"uptime": 123}
