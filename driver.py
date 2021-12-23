import sys
sys.path.append(__file__)

from data.nse import get_nifty500_stocks, stocks_to_ignore
from data.from_yfinance import get_data

# Golden Cross Strategy
from strategy1.main import run as golden_cross
# SMA50 cuts SMA20 from above Strategy
from strategy2.main import run as sma50_200
# Super performance stocks
from strategy3.main import run as super_performant
# Swing trading 44 MA strategy
from strategy4.main import run as swing
# Intra day trading 44 MA strategy
from strategy5.main import run as intra_day
# Golden cross + 44 MA
from strategy6.main import run as golden_cross_with_44ma

strategies = {
    'golden_cross': golden_cross,
    'sma50_200': sma50_200,
    'super_performant': super_performant,
    'swing': swing,
    'intra_day': intra_day,
    'golden_cross_with_44ma': golden_cross_with_44ma
}


def gather_data():
    stocks = [x + ".NS" for x in get_nifty500_stocks()]
    stocks = [x for x in stocks if x not in [x + ".NS" for x in stocks_to_ignore()]]
    for stock in stocks:
        df = get_data(stock, period='350d', interval='1d')


# gather_data()


if len(sys.argv) < 2:
    print("Pass the strategy as first argument\n")
    print("Possible Strategies: ", list(strategies.keys()))
elif len(sys.argv) > 2:
    print("Too many arguments. Only pass one argument as strategy name\n")
    print("Possible Strategies: ", list(strategies.keys()))
elif strategies.get(sys.argv[1]) is not None:
    strategies[sys.argv[1]]()
else:
    print("This strategy is not implemented\n")
    print("Possible Strategies: ", list(strategies.keys()))


