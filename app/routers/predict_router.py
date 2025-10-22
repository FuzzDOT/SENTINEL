from fastapi import APIRouter, HTTPException
from ..schemas import PredictRequest
from ..pipeline.predict import predict_next

router = APIRouter(prefix="/predict", tags=["predict"])

@router.post("")
def predict(req: PredictRequest):
    try:
        return predict_next(req.category, req.symbol, req.days_ahead)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
