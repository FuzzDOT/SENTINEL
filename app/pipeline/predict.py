import os, yaml, numpy as np, pandas as pd, torch, joblib
from ..utils.env import MODEL_DIR
from ..utils.io import model_path, scaler_path
from ..data.sources import fetch_yf, fetch_fred, merge_price_frame
from ..features.technical import compute_features
from .dataset import make_sequences, apply_scaler

from ..models.dl_model import LSTMForecaster

def _device():
    return "cuda" if torch.cuda.is_available() else "cpu"

def load_cfgs():
    with open("configs/model.yaml","r") as f:
        return yaml.safe_load(f)

def _load_model(symbol_key: str, n_features: int) -> LSTMForecaster:
    model = LSTMForecaster(n_features=n_features)
    path = model_path(symbol_key)
    model.load_state_dict(torch.load(path, map_location="cpu"))
    model.eval()
    return model

def predict_next(category: str, symbol: str, days_ahead: int = 5):
    cfg = load_cfgs()
    lookback = int(cfg.get("lookback", 120))

    # fetch & features
    if category in ["stocks","etfs","crypto"]:
        df = fetch_yf(symbol)
    elif category in ["bonds_fred","housing_fred"]:
        df = fetch_fred(symbol)
    else:
        raise ValueError("unknown category")

    feat_df = compute_features(merge_price_frame(df))
    feature_cols = [c for c in feat_df.columns if c not in ["return_1d"]]

    X, y = make_sequences(feat_df, feature_cols, "return_1d", lookback)
    symbol_key = f"{category}__{symbol}"
    scaler = joblib.load(scaler_path(symbol_key))
    X_scaled = apply_scaler(scaler, X)

    model = _load_model(symbol_key, n_features=X.shape[-1])

    device = _device()
    with torch.no_grad():
        x_last = torch.tensor(X_scaled[-1:])  # last window
        pred = model(x_last.to(device)).cpu().numpy().ravel()[0]

    # naive multi-step: assume same predicted 1d return repeated days_ahead
    preds = [float(pred) for _ in range(days_ahead)]
    return {
        "category": category,
        "symbol": symbol,
        "predicted_returns_1d": preds,
        "last_date": str(feat_df.index[-1].date()),
    }
