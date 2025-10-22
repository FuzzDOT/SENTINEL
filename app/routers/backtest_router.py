import pandas as pd
from fastapi import APIRouter, HTTPException
from ..schemas import BacktestRequest
from ..pipeline.predict import predict_next
from ..data.sources import fetch_yf, fetch_fred, merge_price_frame
from ..features.technical import compute_features
from ..backtest.engine import simple_threshold_strategy, backtest

router = APIRouter(prefix="/backtest", tags=["backtest"])

@router.post("")
def run_backtest(req: BacktestRequest):
    try:
        # get historical realized returns
        if req.category in ["stocks","etfs","crypto"]:
            df = fetch_yf(req.symbol)
        else:
            df = fetch_fred(req.symbol)
        feat = compute_features(merge_price_frame(df))
        realized = feat["return_1d"]

        # For MVP, produce in-sample prediction proxy = realized shifted by -1 (or use a trained model offline).
        # In production, you should generate predictions from a trained model across history.
        # Here we emulate with a simple rolling mean of returns to create a pseudo-prediction series.
        pred_proxy = realized.rolling(5).mean().shift(1).dropna()
        sig = simple_threshold_strategy(pred_proxy, req.long_threshold, req.short_threshold)
        report = backtest(realized.loc[pred_proxy.index], sig)

        return {"metrics": report}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
