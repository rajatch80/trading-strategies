import yfinance as yf


def get_data(ticker, period="1mo", interval="1d", start=None, end=None):
    if start is not None and end is not None:
        data = yf.download(ticker, start=start, end=end, interval=interval)
    else:
        data = yf.download(ticker, period=period, interval=interval)
    data.dropna(how="any", inplace=True)
    return data
