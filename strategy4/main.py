"""
This finds super performer stocks a/c to Rising Moving Average 44 and tells entry point
Criteria:
    1. Moving Average 44 should be rising, not falling or sideways
    2. Time frame is Daily
    3. The Last day should have green candle stick
    4. The last price should be near the 44 Moving Average
"""
import os
import csv
from datetime import datetime
from pprint import pprint

from data.yfinance import get_data
from data.nse import (
    get_top_stocks_by_market_cap,
    get_nifty50_stocks,
    get_nifty500_stocks,
    get_bad_stocks
)


def get_price_data(tickers):
    ohlc_data = {}
    for ticker in tickers:
        ohlc_data[ticker] = get_data(ticker, period='350d', interval='1d')
        # start = '2021-01-01'
        # end = '2021-11-30'
        # ohlc_data[ticker] = get_data(ticker, start=start, end=end, interval='1d')
    return ohlc_data


def is_stock_rising(df):
    last_14_days_trend = df['44MA'][-14:].to_list()
    # 44 MA should go up for last 14 consecutive days
    return sorted(last_14_days_trend) == last_14_days_trend


def is_probable_buy(df):
    # check for red candle, skip
    if df['Open'][-1] >= df['Close'][-1]:
        return
    high = df['High'][-1]
    low = df['Low'][-1]
    # 44 MA should lie between green candle's high-low range +- 1%
    return (low - .02 * low) <= df['44MA'][-1] <= (high + .02 * high)


def calculate_buy_details(stock, df):
    entry = round(1.001 * df['High'][-1])
    stop_loss = round(0.999 * min(df['Low'][-1], df['Low'][-2]))
    if entry == stop_loss:
        return
    risk = 500
    quantity = round(risk / (entry - stop_loss))
    target = 2 * (entry - stop_loss) + entry
    money_to_trade = round(entry) * quantity + 1
    return {
        'stock': stock.split(".")[0],
        'entry': entry,
        'stop_loss': stop_loss,
        'quantity': quantity,
        'target': target,
        'money_to_trade': money_to_trade,
    }


def export_to_csv(trades):
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = curr_dir + "/" + datetime.today().strftime('%d-%m-%Y') + "-TRADES.csv"
    with open(file_name, "w", newline="") as f:
        title = "stock,entry,stop_loss,target,quantity,money_to_trade".split(",")
        cw = csv.DictWriter(f, title, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        cw.writeheader()
        cw.writerows(trades)


def get_trades():
    stocks = [x + ".NS" for x in get_nifty50_stocks()] + \
             [x + ".NS" for x in get_top_stocks_by_market_cap()] + \
             [x + ".NS" for x in get_nifty500_stocks()]
    stocks = [x for x in stocks if x not in get_bad_stocks()]
    stocks = list(set(stocks))
    trades = []
    for stock in stocks:
        try:
            df = get_data(stock, period='350d', interval='1d')
            # Add 44 Moving Average
            df['44MA'] = df['Close'].rolling(window=44).mean()
            if not is_stock_rising(df):
                continue
            if not is_probable_buy(df):
                continue
            buy_details = calculate_buy_details(stock, df)
            if buy_details is None:
                continue
            print("TRADE FOUND >>>>>>>>>>>>>>>>>>>>>>>\n")
            print("STOCK: ------   " + stock + "    -------")
            pprint(buy_details)
            print("===================================\n")
            trades.append(buy_details)
        except Exception as e:
            print("Exception occurred >>>>>>>>>>>>>>>>>>>>>>>\n")
            print(e)
    return trades


def run():
    trades = get_trades()
    pprint(trades)
    # optional, comment if not needed
    try:
        export_to_csv(trades)
    except Exception as e:
        print("FAILED TO EXPORT TO CSV")
        print(e)
