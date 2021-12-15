"""
This code finds the golden cross (where 44 MA crosses 200 MA from below)
"""
import csv
import os
from datetime import datetime
from pprint import pprint

from data.nse import (
    get_nifty100_stocks,
    get_nifty50_stocks,
    get_nifty500_stocks,
    stocks_to_ignore
)
from data.from_yfinance import get_data


def find_golden_cross(df):
    return


def is_44_rising(df):
    return


def is_200_rising(df):
    return


def get_trades(stocks):
    trades = {}
    for stock in stocks:
        df = get_data(stock, period="350d", interval="1d")
        df['44MA'] = df['Close'].rolling(window=44).mean()
        df['200MA'] = df['Close'].rolling(window=200).mean()
        golden_cross = find_golden_cross(df)
        print(golden_cross)
        if is_44_rising(df) and is_200_rising(df):
            trades[stock] = df
    return trades


def run():
    stocks = [x + ".NS" for x in get_nifty50_stocks()]
    # [x + ".NS" for x in get_nifty100_stocks()] + \
    # [x + ".NS" for x in get_nifty500_stocks()]
    stocks = [x for x in stocks if x not in [x + ".NS" for x in stocks_to_ignore()]]
    stocks = list(set(stocks))
    print(len(stocks), " Stock are getting scanned")
    trades = get_trades(stocks)
    pprint(trades)
    # optional, comment if not needed
    # export_to_csv(trades)
