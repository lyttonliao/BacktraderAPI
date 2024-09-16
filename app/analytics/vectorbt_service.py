import vectorbt as vbt
import pandas as pd
import numpy as np
import datetime

from typing import Optional, Dict, List


def price_data(
    symbol: str, 
    start_time: str, 
    end_time: str, 
    interval: str,
):
    """Downloads data Yahoo Finance through VectorBT's API"""
    yf_data = vbt.YFData.download_symbol(
        symbol,
        interval,
        start=start_time,
        end=end_time,
    )

    return yf_data


def add_rsi_indicator(close: List[int], window: int, entry: float = 20.00, exit: float = 80.00):
    """Add a relative strength index indicator to the custom strategy"""

    rsi = vbt.RSI.run(close, window)
    rsi_df = rsi.rsi
    fig = rsi.plot(levels=(entry, exit))
    entries = rsi_df < entry
    exits = rsi_df > exit

    return entries, exits, fig


def add_ma_indicator(close: List[int], window: Optional[int] = None, fast_window: Optional[int] = None, slow_window: Optional[int] = None):
    "Add a moving average index indicator to the custom strategy"

    print(window, slow_window, fast_window)
    if window:
        ma = vbt.MA.run(close, window)
        entries = ma.ma_crossed_above(close)
        exits = ma.ma_crossed_below(close)
        fig = ma.plot()
    else:
        fast_ma = vbt.MA.run(close, fast_window)
        slow_ma = vbt.MA.run(close, slow_window)
        entries = fast_ma.ma_crossed_above(slow_ma.ma)
        exits = fast_ma.ma_crossed_below(slow_ma.ma)
        fig = fast_ma.plot(ma_trace_kwargs=dict(name=f'Fast MA ({fast_window})'))
        fig = slow_ma.plot(fig=fig, ma_trace_kwargs=dict(name=f'Slow MA ({slow_window})'))

    return exits, entries, fig


def add_stoch_indicator(close: List[int], high: List[int], low: List[int], k_window: int, d_window: int, entry: int = 20, exit: int = 80):
    """Add a stochastic oscillator indicator to the custom strategy"""

    stoch = vbt.STOCH.run(close, high, low, k_window, d_window)
    stoch_k = stoch.percent_k
    stoch_d = stoch.percent_d
    entries = stoch.percent_k_crossed_above(stoch_d) | stoch_k < entry
    exits = stoch.percent_k_crossed_below(stoch_d) | stoch_k > exit
    fig = stoch.plot(levels=(entry, exit))
    return entries, exits, fig


def add_bbands_indicator(close: List[int], window: int = 20, alpha: int = 2):
    """Add a bollinger bands indicator to the custom strategy, currently supports basic bollinger actions, does not trace contraction or expansion of the bands"""

    bbands = vbt.BBANDS.run(close, window, alpha)
    lower = bbands.lower
    lower_shifted = bbands.lower.shift(-1)
    upper = bbands.upper
    upper_shifted = bbands.upper.shift(-1)
    entries = bbands.close_below(lower) & bbands.close_above(lower_shifted)
    exits = bbands.close_above(upper) & bbands.close_below(upper_shifted)
    fig = bbands.plot()
    fig.show()
    return entries, exits, fig


def add_atr_indicator(close: List[int], high: List[int], low: List[int], window: int = 14, trailing_stop: int = 2):
    """Add an average true range indicator to the custom strategy"""

    atr = vbt.ATR.run(close, high, low, window)
    atr_val = atr.atr
    trigger = close + atr_val
    stop_limit = close - atr_val * trailing_stop
    trigger_shifted = trigger.shift(1)
    entries = atr.close_crossed_above(trigger_shifted)
    exits = atr.close_crossed_below(stop_limit)
    fig = atr.plot()
    return entries, exits, fig


indicator_map = {
    'rsi': add_rsi_indicator,
    'ma': add_ma_indicator,
    'stoch': add_stoch_indicator,
    'bbands': add_bbands_indicator,
    'atr': add_atr_indicator
}


def run_strategy_handler(
    symbol: List[str],
    start_time: str,
    data: Dict[str, List[Dict]],
    end_time: str = datetime.datetime.now(),
    interval: str = 'max',
):
    """Use VectorBT's Indicator Factory API to construct a custom indicator/strategy"""

    prices = price_data(
        symbol=symbol,
        start_time=start_time,
        end_time=end_time,
        interval=interval,
    )

    entries = pd.DataFrame()
    exits = pd.DataFrame()
    figs = []

    for ind_type, inds in data.items():
        fn = indicator_map[ind_type]

        for ind in inds:
            inputs = [prices[input_name] for input_name in ind['inputs']]
            new_entries, new_exits, fig = fn(*inputs, **ind['params'])
            figs.append(fig)
            if entries.empty and exits.empty:
                entries = new_entries
                exits = new_exits
            else:
                entries = entries & new_entries
                exits = exits & new_exits

    pf = vbt.Portfolio.from_signals(prices["Close"], entries, exits)

    return pf, figs

symbol = "TSLA"
end_time = datetime.datetime.now()
start_time = end_time - datetime.timedelta(days=365)
data = {
    'rsi': [
        # {
        #     'inputs': ['Close'],
        #     'params': {
        #         'exit': 80,
        #         'entry': 20,
        #         'window': 20
        #     }
        # },
    ],
    'ma': [
        # {
        #     'inputs': ['Close'],
        #     'params': {
        #         'window': 20
        #     },
        # },
        # {
        #     'inputs': ['Close'],
        #     'params': {
        #         'fast_window': 10,
        #         'slow_window': 30
        #     },
        # }
    ],
    'stoch': [
        # {
        #     'inputs': ['Close', 'Low', 'High'],
        #     'params': {
        #         'entry': 20,
        #         'exit': 80,
        #         'k_window': 14,
        #         'd_window': 3,
        #     }
        # }
    ],
    'bbands': [
        {
            'inputs': ['Close'],
            'params': {
                'window': 20,
                'alpha': 1.5
            }
        }
    ],
    'atr': [],
}

print(run_strategy_handler(symbol=symbol, start_time=start_time, data=data))