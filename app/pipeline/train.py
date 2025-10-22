import yaml, os
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, Optional
from sklearn.metrics import mean_squared_error
import torch
from torch.utils.data import TensorDataset, DataLoader
from ..utils.env import DATA_DIR, MODEL_DIR
from ..utils.io import model_path, scaler_path, save_json
from ..data.sources import fetch_yf, fetch_fred, merge_price_frame
from ..features.technical import compute_features
from .dataset import make_sequences, fit_scaler, apply_scaler
from ..models.dl_model import LSTMForecaster

def _device():
    return "cuda" if torch.cuda.is_available() else "cpu"

def load_configs() -> Tuple[Dict[str, Any], Dict[str, Any]]:
    with open("configs/model.yaml", "r") as f:
        model_cfg = yaml.safe_load(f) or {}
    with open("configs/assets.yaml", "r") as f:
        assets_cfg = yaml.safe_load(f) or {}
    return model_cfg, assets_cfg

def get_series(category: str, symbol: str) -> pd.DataFrame:
    if category in ["stocks", "etfs", "crypto"]:
        df = fetch_yf(symbol)
    elif category in ["bonds_fred", "housing_fred"]:
        df = fetch_fred(symbol)
    else:
        raise ValueError(f"Unknown category {category}")
    return merge_price_frame(df)

def train_symbol(category: str, symbol: str, overrides: Optional[Dict[str,Any]] = None) -> Dict[str,Any]:
    model_cfg, _ = load_configs()
    if overrides is not None:
        if not isinstance(overrides, dict):
            raise TypeError("overrides must be a dict")
        model_cfg.update(overrides)

    horizon = int(model_cfg.get("horizon", 5))
    lookback = int(model_cfg.get("lookback", 120))
    epochs = int(model_cfg.get("epochs", 15))
    lr = float(model_cfg.get("lr", 1e-3))
    batch_size = int(model_cfg.get("batch_size", 64))
    target_col = model_cfg.get("target", "return_1d")
    price_df = get_series(category, symbol)
    feat_df = compute_features(price_df)

    feature_cols = [c for c in feat_df.columns if c not in ["return_1d"]]
    # Build sequences
    X, y = make_sequences(feat_df, feature_cols, target_col, lookback)
    if len(X) < 200:
        raise ValueError("Not enough data after feature engineering to train.")

    # Split train/test (time based)
    test_days = int(model_cfg.get("train",{}).get("test_size_days",365))
    # approximate index split by date
    cutoff_date = feat_df.index[-1] - pd.Timedelta(days=test_days)
    cutoff_idx = np.searchsorted(feat_df.index[lookback:], cutoff_date)  # index in X
    cutoff_idx = max(1, min(cutoff_idx, len(X)-1))

    X_train, y_train = X[:cutoff_idx], y[:cutoff_idx]
    X_test, y_test = X[cutoff_idx:], y[cutoff_idx:]

    # Scale
    scaler = fit_scaler(X_train)
    X_train = apply_scaler(scaler, X_train)
    X_test  = apply_scaler(scaler, X_test)

    device = _device()
    model = LSTMForecaster(n_features=X.shape[-1]).to(device)

    train_ds = TensorDataset(torch.tensor(X_train), torch.tensor(y_train).unsqueeze(-1))
    test_ds  = TensorDataset(torch.tensor(X_test), torch.tensor(y_test).unsqueeze(-1))
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    test_loader  = DataLoader(test_ds, batch_size=batch_size, shuffle=False)

    optim = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = torch.nn.MSELoss()

    for epoch in range(1, epochs+1):
        model.train()
        epoch_loss = 0.0
        for xb, yb in train_loader:
            xb, yb = xb.to(device), yb.to(device)
            optim.zero_grad()
            preds = model(xb)
            loss = loss_fn(preds, yb)
            loss.backward()
            optim.step()
            epoch_loss += loss.item()*len(xb)
        epoch_loss /= len(train_ds)

    # Evaluate
    model.eval()
    with torch.no_grad():
        preds = []
        trues = []
        for xb, yb in test_loader:
            xb = xb.to(device)
            out = model(xb).cpu().numpy().ravel()
            preds.append(out)
            trues.append(yb.numpy().ravel())
        y_pred = np.concatenate(preds)
        y_true = np.concatenate(trues)
    mse = mean_squared_error(y_true, y_pred)
    rmse = float(np.sqrt(mse))

    # Save artifacts
    os.makedirs(MODEL_DIR, exist_ok=True)
    torch.save(model.state_dict(), model_path(f"{category}__{symbol}"))
    import joblib
    joblib.dump(scaler, scaler_path(f"{category}__{symbol}"))

    report = {
        "category": category,
        "symbol": symbol,
        "samples_train": int(len(X_train)),
        "samples_test": int(len(X_test)),
        "rmse_test": float(rmse),
        "feature_cols": feature_cols,
        "lookback": lookback,
        "target": target_col,
    }
    save_json(os.path.join(MODEL_DIR, f"{category}__{symbol}_report.json"), report)
    return report
