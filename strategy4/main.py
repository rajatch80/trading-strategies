"""
This finds super performer stocks a/c to Rising Moving Average 44 and tells entry point
Criteria:
    1. Moving Average 44 should be rising, not falling or sideways
    2. Time frame is Daily
    3. The Last day should have green candle stick
    4. The last price should be near the 44 Moving Average
"""
import pandas as pd
import datetime as dt
from pprint import pprint

from data.yfinance import get_data
from data.nse import get_top_stocks_by_market_cap
from data.nse import get_nifty50_tickers


def get_price_data(tickers):
    ohlc_data = {}
    for ticker in tickers:
        ohlc_data[ticker] = get_data(ticker, period='350d', interval='1d')
        # start = '2021-01-01'
        # end = '2021-11-30'
        # ohlc_data[ticker] = get_data(ticker, start=start, end=end, interval='1d')
    return ohlc_data


def find_rising_tickers():
    tickers = [x + ".NS" for x in get_nifty50_tickers()] + [x + ".NS" for x in get_top_stocks_by_market_cap()]
    # tickers = ['ADANIENT.NS', 'DMART.NS', 'BHARTIARTL.NS', 'BOSCHLTD.NS', 'MCDOWELL-N.NS', 'PGHH.NS', 'NTPC.NS',
    #           'TATAMOTORS.NS', 'TECHM.NS', 'LT.NS', 'HINDPETRO.NS', 'TITAN.NS', 'LTI.NS', 'M&M.NS', 'IOC.NS',
    #           'POWERGRID.NS', 'BAJAJHLDNG.NS', 'BANKBARODA.NS', 'ICICIBANK.NS', 'DLF.NS', 'ADANIGREEN.NS',
    #           'GRASIM.NS', 'BANDHANBNK.NS', 'MARUTI.NS', 'INDUSTOWER.NS', 'VEDL.NS', 'SBIN.NS', 'ONGC.NS']
    # tickers = ['TATAMOTORS.NS']
    tickers = list(set(tickers))
    ohlc_data = get_price_data(tickers)
    rising_44_ma_stocks = []
    for ticker in tickers:
        ohlc_data[ticker]['44MA'] = ohlc_data[ticker]['Close'].rolling(window=44).mean()
        last_14_days_trend = ohlc_data[ticker]['44MA'][-14:].to_list()
        if sorted(last_14_days_trend) == last_14_days_trend:
            rising_44_ma_stocks.append(ticker)
    return {ticker: ohlc_data[ticker] for ticker in rising_44_ma_stocks}


def get_probable_buys(stocks):
    probable_buys = {}
    for ticker, df in stocks.items():
        last_open = df['Open'][-1]
        last_close = df['Close'][-1]
        if last_open >= last_close:
            continue
        if (last_open - .03 * last_open) <= df['44MA'][-1] <= (last_close + .03 * last_close):
            probable_buys[ticker] = df
    return probable_buys


def get_buy_details(stocks):
    trading_details = {}
    # risk to reward ratio 1:2
    for ticker, df in stocks.items():
        entry = round(1.001 * df['High'][-1])
        stop_loss = round(0.999 * min(df['Low'][-1], df['Low'][-2]))
        risk = 500
        quantity = round(risk / (entry - stop_loss))
        target = 2 * (entry - stop_loss) + entry
        money_to_trade = round(entry) * quantity + 1
        trading_details[ticker] = {
            'entry': entry,
            'stop_loss': stop_loss,
            'quantity': quantity,
            'target': target,
            'money_to_trade': money_to_trade,
        }
    return trading_details


def run():
    stocks = find_rising_tickers()
    # print(stocks)
    probable_buys = get_probable_buys(stocks)
    trading_details = get_buy_details(probable_buys)
    pprint(trading_details)
