import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from typing import Tuple

def make_sequences(df: pd.DataFrame, feature_cols, target_col: str, lookback: int) -> Tuple[np.ndarray, np.ndarray]:
    X, y = [], []
    for i in range(lookback, len(df)):
        X.append(df[feature_cols].iloc[i-lookback:i].values)
        y.append(df[target_col].iloc[i])
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)

def fit_scaler(train_feats: np.ndarray) -> StandardScaler:
    B, T, F = train_feats.shape
    reshaped = train_feats.reshape(B*T, F)
    scaler = StandardScaler()
    scaler.fit(reshaped)
    return scaler

def apply_scaler(scaler, feats: np.ndarray) -> np.ndarray:
    B, T, F = feats.shape
    reshaped = feats.reshape(B*T, F)
    scaled = scaler.transform(reshaped)
    return scaled.reshape(B, T, F)
