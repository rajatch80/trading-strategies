"""
Relative Strength Index
"""


def SMA(DF, period=30, column='Close'):
    df = DF.copy()
    return df[column].rolling(window=period).mean()
