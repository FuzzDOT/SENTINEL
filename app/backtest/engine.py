import numpy as np
import pandas as pd

def simple_threshold_strategy(pred_returns: pd.Series, long_th: float, short_th: float) -> pd.Series:
    sig = pd.Series(0, index=pred_returns.index, dtype=int)
    sig[pred_returns > long_th] = 1
    sig[pred_returns < short_th] = -1
    return sig

def backtest(returns: pd.Series, signals: pd.Series, txn_cost_bps: float = 5.0) -> dict:
    # Align
    idx = returns.index.intersection(signals.index)
    returns = returns.loc[idx]
    signals = signals.loc[idx].shift(1).fillna(0)  # trade at next open (one-step lag)

    gross = signals * returns
    costs = signals.diff().abs().fillna(0).astype(float) * (txn_cost_bps / 10000.0)
    net = gross - costs

    equity = (1 + net).cumprod()
    cagr = equity.iloc[-1]**(252/len(equity)) - 1 if len(equity) > 0 else 0.0
    base_std = net.std()
    vol = base_std * np.sqrt(252)
    sharpe = (net.mean() / base_std * np.sqrt(252)) if base_std > 0 else 0.0
    mdd = (equity / equity.cummax() - 1).min()

    return {
        "cagr": float(cagr),
        "sharpe": float(sharpe),
        "volatility": float(vol),
        "max_drawdown": float(mdd),
        "final_equity": float(equity.iloc[-1] if len(equity)>0 else 1.0),
    }
