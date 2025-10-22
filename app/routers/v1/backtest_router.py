from fastapi import APIRouter

router = APIRouter(prefix="/backtest")


@router.post("/run")
def run_backtest():
    return {"status": "started"}
