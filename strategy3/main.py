"""
this finds super performer stocks
Criteria:
    1. Current stock price is above the 150 and 200 days moving average (MA).
    2. The 150 days moving average is above the 200 days moving average.
    3. The 200 days moving average is trending up for at least a month.
    4. The 50 day MA is above the 150 and 200 MAs
    5. Stock price is above the 50 day MA
    6. Current share price is at least 30% above its 52 week low
    7. Current stock price is at least within 25% of the 52 week high
"""
import pandas as pd

from data.from_yfinance import get_data
from data.nse import get_nifty100_stocks
from data.nse import get_nifty50_stocks
from indicators.SMA import SMA


def get_price_df(tickers):
    df = get_data("^NSEI", period='350d', interval='1d')
    df = df[['Close']]
    df.rename(columns={'Close': "^NSEI"}, inplace=True)
    for ticker in tickers[1:]:
        df_ = get_data(ticker, period='350d', interval='1d')
        df[ticker] = df_[['Close']]
    return df


def get_metrics_df():
    tickers = ["^NSEI"] + [x + ".NS" for x in get_nifty50_stocks()]
    df = get_price_df(tickers)
    print(df)
    metrics = {}
    for ticker in tickers:
        metrics[ticker] = {}
        df['200MA'] = df[ticker].rolling(window=200).mean()
        df['150MA'] = df[ticker].rolling(window=150).mean()
        df['50MA'] = df[ticker].rolling(window=50).mean()
        df['RS'] = (df[ticker][-1] / df['^NSEI'][-1]) / (df[ticker][-252] / df['^NSEI'][-252]) * 100

        metrics[ticker]['200MA'] = df['200MA'][-1]
        metrics[ticker]['150MA'] = df['150MA'][-1]
        metrics[ticker]['50MA'] = df['50MA'][-1]
        metrics[ticker]['200MA_1mago'] = df['200MA'][-30]
        metrics[ticker]['150MA_1mago'] = df['150MA'][-30]
        metrics[ticker]['200MA_2mago'] = df['200MA'][-60]
        metrics[ticker]['150MA_2mago'] = df['150MA'][-60]
        metrics[ticker]['52W_Low'] = df[ticker][-252:].min()
        metrics[ticker]['52W_High'] = df[ticker][-252:].max()
        metrics[ticker]['price'] = df[ticker][-1]
        metrics[ticker]['Relative Strength'] = df['RS'][-1]
        # Current Price is at least 30% above 52 week low (1.3*low_of_52week)
        metrics[ticker]['Above_30%_low'] = metrics[ticker]['52W_Low'] * 1.3
        # Condition 7: Current Price is within 25% of 52 week high   (.75*high_of_52week)
        metrics[ticker]['Within_25%_high'] = metrics[ticker]['52W_High'] * 0.75

    metrics_df = pd.DataFrame.from_dict(metrics)
    metrics_df = metrics_df.T
    # to determine the rank percentile and see which are the 80% top performers
    metrics_df['pct_rank'] = metrics_df['Relative Strength'].rank(pct=True)
    metrics_df = metrics_df.T
    # metrics_df.to_csv('strategy3/nifty50.csv')
    return metrics_df


def run():
    metrics_df = get_metrics_df()
    metrics_df = metrics_df.T
    stocks = metrics_df[1:]
    stocks['condition1'] = (stocks['price'] > stocks['200MA']) & (stocks['price'] > stocks['150MA'])

    stocks['condition2'] = stocks['150MA'] > stocks['200MA']
    # 3 The 200-day moving average line is trending up for 1 month
    stocks['condition3'] = stocks['200MA'] > stocks['200MA_1mago']
    stocks['condition4'] = (stocks['50MA'] > stocks['200MA']) & (stocks['50MA'] > stocks['150MA'])
    stocks['condition5'] = stocks['price'] > stocks['50MA']
    # 6 The current stock price is at least 30 percent above its 52-week low
    stocks['condition6'] = stocks['price'] > stocks['Above_30%_low']
    # 7 The current stock price is within at least 25 percent of its 52-week high.
    stocks['condition7'] = stocks['price'] > stocks['Within_25%_high']
    # 8 The relative strength ranking is above 80
    stocks['condition8'] = stocks['pct_rank'] > 0.8

    selection = stocks[
        (stocks['condition1'] == True) &
        (stocks['condition2'] == True) &
        (stocks['condition3'] == True) &
        (stocks['condition4'] == True) &
        (stocks['condition5'] == True) &
        (stocks['condition6'] == True) &
        (stocks['condition7'] == True) &
        (stocks['condition8'] == True)
    ]

    print(selection)
