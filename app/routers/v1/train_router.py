from fastapi import APIRouter

router = APIRouter(prefix="/train")


@router.post("/")
def start_train():
    return {"status": "queued"}
