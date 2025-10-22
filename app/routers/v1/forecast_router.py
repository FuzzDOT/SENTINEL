from fastapi import APIRouter

router = APIRouter(prefix="/forecast")


@router.post("/")
def run_forecast():
    return {"status": "running"}
