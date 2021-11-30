"""
This tells buy and sell points.
Criteria:
- If SMA50 cuts SMA20 from above: Buy, otherwise Sell
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

from data.yfinance import get_data
from indicators.SMA import SMA


def plot(df, title):
    plt.figure(figsize=(16, 8))
    plt.title(title, fontsize=18)
    plt.plot(df['Close'], alpha=0.5, label='Close')
    plt.plot(df['SMA20'], alpha=0.5, label='SMA20', color='yellow')
    plt.plot(df['SMA50'], alpha=0.5, label='SMA50')
    plt.scatter(df.index, df['Buy'], alpha=1, label='Buy Signal', marker='^', color='green')
    plt.scatter(df.index, df['Sell'], alpha=1, label='Sell Signal', marker='v', color='red')
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Close Price', fontsize=18)
    plt.show()


def run():
    df = get_data('HDFCBANK.NS', period="2y", interval="1d")
    df['SMA20'] = SMA(df, period=20)
    df['SMA50'] = SMA(df, period=50)
    df['Signal'] = np.where(df['SMA20'] > df['SMA50'], 1, 0)
    df['Position'] = df['Signal'].diff()

    df['Buy'] = np.where(df['Position'] == 1, df['Close'], np.NAN)
    df['Sell'] = np.where(df['Position'] == -1, df['Close'], np.NAN)

    print(df)
    plot(df, 'Close Price History w/ Buy & Sell Signals')
    # print(data)
