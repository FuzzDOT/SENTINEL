from fastapi import APIRouter, HTTPException
from ..schemas import TrainRequest, TrainReport
from ..pipeline.train import train_symbol

router = APIRouter(prefix="/train", tags=["train"])

@router.post("", response_model=TrainReport)
def train(req: TrainRequest):
    try:
        report = train_symbol(req.category, req.symbol)
        return report
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
