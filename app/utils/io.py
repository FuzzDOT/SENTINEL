import os, json, joblib
from typing import Any
from .env import MODEL_DIR

def model_path(symbol: str) -> str:
    safe = symbol.replace("/", "_")
    return os.path.join(MODEL_DIR, f"{safe}.pt")

def scaler_path(symbol: str) -> str:
    safe = symbol.replace("/", "_")
    return os.path.join(MODEL_DIR, f"{safe}_scaler.gz")

def save_json(path: str, obj: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
