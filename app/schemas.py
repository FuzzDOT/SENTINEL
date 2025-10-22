from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class TrainRequest(BaseModel):
    category: str = Field(..., description="stocks|etfs|crypto|bonds_fred|housing_fred")
    symbol: str

class PredictRequest(BaseModel):
    category: str
    symbol: str
    days_ahead: int = 5

class BacktestRequest(BaseModel):
    category: str
    symbol: str
    long_threshold: float = 0.001
    short_threshold: float = -0.001
    txn_cost_bps: float = 5.0

class TrainReport(BaseModel):
    category: str
    symbol: str
    samples_train: int
    samples_test: int
    rmse_test: float
    feature_cols: List[str]
    lookback: int
    target: str
