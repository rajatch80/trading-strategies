import sys
sys.path.append(__file__)
# Golden Cross Strategy
from strategy1.main import run as run_strategy1
# SMA50 cuts SMA20 from above Strategy
from strategy2.main import run as run_strategy2
# Super performance stocks
from strategy3.main import run as run_strategy3
# Swing trading 44 MA strategy
from strategy4.main import run as run_strategy4
# Intra day trading 44 MA strategy
from strategy5.main import run as run_strategy5
# Golden cross + 44 MA
from strategy6.main import run as run_strategy6

strategies = {
    'golden_cross': run_strategy1,
    'sma50_200': run_strategy2,
    'super_performant': run_strategy3,
    'swing': run_strategy4,
    'intra_day': run_strategy5,
    'golden_cross_with_44ma': run_strategy6
}


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


