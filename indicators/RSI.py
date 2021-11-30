"""
Relative Strength Index
"""
import numpy as np


def RSI(DF, n=14):
    df = DF.copy()
    df["Change"] = df["Adj Close"] - df["Adj Close"].shift(1)
    df["Gain"] = np.where(df["Change"] >= 0, df["Change"], 0)
    df["Loss"] = np.where(df["Change"] <= 0, -1 * df["Change"], 0)
    df["AvgGain"] = df["Gain"].ewm(alpha=1 / n, min_periods=n).mean()
    df["AvgLoss"] = df["Loss"].ewm(alpha=1 / n, min_periods=n).mean()
    df["RS"] = df["AvgGain"] / df["AvgLoss"]
    df["RSI"] = 100 - (100 / (1 + df["RS"]))

    return df["RSI"]
