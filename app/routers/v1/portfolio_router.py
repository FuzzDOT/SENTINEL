from fastapi import APIRouter

router = APIRouter(prefix="/portfolio")


@router.get("/positions")
def list_positions():
    return {"positions": []}
