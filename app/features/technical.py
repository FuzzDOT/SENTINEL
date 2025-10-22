import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import BollingerBands

def compute_features(price_df: pd.DataFrame) -> pd.DataFrame:
    df = price_df.copy()
    df["returns_1d"] = df["price"].pct_change()
    df["volatility_10d"] = df["returns_1d"].rolling(10).std()
    # SMA
    df["sma_10"] = df["price"].rolling(10).mean()
    # RSI (14)
    df["rsi_14"] = RSIIndicator(close=df["price"], window=14).rsi()
    # MACD
    macd = MACD(close=df["price"])
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    # Bollinger Bands
    bb = BollingerBands(close=df["price"], window=20, window_dev=2)
    df["bb_high"] = bb.bollinger_hband()
    df["bb_low"] = bb.bollinger_lband()
    df["bb_width"] = (df["bb_high"] - df["bb_low"]) / df["price"]
    df["bb_width"] = (df["bb_high"] - df["bb_low"]) / df["price"]
    # Targets
    df["return_1d"] = df["price"].pct_change().shift(-1)
    df = df.dropna().astype(float)
    return df
