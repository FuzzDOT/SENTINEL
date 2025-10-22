from fastapi import APIRouter

router = APIRouter(prefix="/diagnostics")


@router.get("/healthz")
def healthz():
    return {"ok": True}
