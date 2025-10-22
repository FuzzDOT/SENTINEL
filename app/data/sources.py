import pandas as pd
import yfinance as yf
from fredapi import Fred
from datetime import datetime, timedelta
from ..utils.env import FRED_API_KEY

def fetch_yf(ticker: str, period: str = "max", interval: str = "1d") -> pd.DataFrame:
    df = yf.download(ticker, period=period, interval=interval, auto_adjust=True, progress=False)
    if not isinstance(df, pd.DataFrame) or df.empty:
        raise ValueError(f"No data for ticker {ticker}")
    df.index = pd.to_datetime(df.index)
    df = df.rename(columns={"Adj Close": "AdjClose"})
    return df

def fetch_fred(series_id: str, start: str = "1900-01-01") -> pd.DataFrame:
    if not FRED_API_KEY:
        raise ValueError("FRED_API_KEY missing; set it in environment to use FRED series")
    fred = Fred(api_key=FRED_API_KEY)
    s = fred.get_series(series_id, observation_start=start)
    df = pd.DataFrame({"value": s})
    df.index.name = "Date"
    df.index = pd.to_datetime(df.index)
    return df

def merge_price_frame(df: pd.DataFrame) -> pd.DataFrame:
    # Normalize to have standard columns
    out = pd.DataFrame(index=df.index)
    if "AdjClose" in df.columns:
        out["price"] = df["AdjClose"]
    elif "Close" in df.columns:
        out["price"] = df["Close"]
    elif "value" in df.columns:
        out["price"] = df["value"]
    else:
        # fallback: try first numeric column
        out["price"] = df.select_dtypes("number").iloc[:,0]
    return out.dropna()
