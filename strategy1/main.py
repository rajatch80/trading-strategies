"""
Golden cross strategy
"""

import os, sys, argparse
import math
import backtrader as bt
import pandas as pd
from data.from_yfinance import get_data


class GoldenCross(bt.Strategy):
    params = (('fast', 50), ('slow', 200), ('order_percentage', 0.95), ('ticker', 'SPY'))

    def __init__(self):
        self.size = 0
        self.fast_ma = bt.indicators.SMA(
            self.data.close, period=self.params.fast, plotname='50 day moving average'
        )
        self.slow_ma = bt.indicators.SMA(
            self.data.close, period=self.params.slow, plotname='200 day moving average'
        )
        self.crossover = bt.indicators.CrossOver(
            self.fast_ma, self.slow_ma
        )

    def next(self):
        if self.position.size == 0:
            if self.crossover > 0:
                # golden cross happens
                amt_to_invest = self.params.order_percentage * self.broker.cash
                self.size = math.floor(amt_to_invest / self.data.close)
                print("Buy {} shares of {} at {}".format(self.size, self.params.ticker, self.data.close[0]))

                self.buy(size=self.size)

        if self.position.size > 0:
            if self.crossover < 0:
                print("Sell {} shares of {} at {}".format(self.size, self.params.ticker, self.data.close[0]))
                self.close()


def run():
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000)

    spy_prices = get_data('SPY', period='1950d', interval='1d')

    feed = bt.feeds.PandasData(dataname=spy_prices)
    cerebro.adddata(feed)

    cerebro.addstrategy(GoldenCross)

    cerebro.run()
    cerebro.plot()
