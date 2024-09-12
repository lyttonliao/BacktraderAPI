import vectorbt as vbt
import pandas as pd
import numpy as np
import datetime

from typing import Optional, Dict, List


def price_data(
    symbols: List[str], 
    start_time: str, 
    end_time: str, 
    interval: str,
    input_names: List[str]
):
    """Downloads data Yahoo Finance through VectorBT's API"""

    data = vbt.YFData.download(
        symbols=symbols,
        start=start_time,
        end=end_time,
        missing_index='drop',
        interval=interval).get(*input_names)
    
    return data


def add_rsi_indicator(close: List[int], window: int, trend = None, entry: int = 20, exit: int = 80):
    """Add a relative strength index indicator to the custom strategy"""

    rsi = vbt.RSI.run(close, window=window).rsi.to_numpy()
    trend = np.where(rsi > exit, -1, trend if trend else 0)
    trend = np.where(rsi < entry, 1, trend)
    return trend


def add_ma_indicator(close: List[int], window: int, trend = None):
    "Add a moving average index indicator to the custom strategy"

    ma = vbt.MA.run(close, window=window).ma.to_numpy()
    trend = np.where(close < ma, 1, trend if trend else 0)
    return trend


def add_stoch_indicator(close: List[int], high: List[int], low: List[int], k_window: int, d_window: int, trend = None, entry: int = 20, exit: int = 80):
    """Add a stochastic oscillator indicator to the custom strategy"""

    stoch = vbt.STOCH.run(close, high=high, low=low, k_window=k_window, d_window=d_window).stoch.to_numpy()
    trend = np.where(stoch > exit, -1, trend if trend else 0)
    trend = np.where(stoch < entry, 1, trend)
    return trend


def add_bbands_indicator(close: List[int], window: int = 20, trend = None, alpha: int = 2):
    """Add a bollinger bands indicator to the custom strategy, currently supports basic bollinger actions, does not trace contraction or expansion of the bands"""

    bbands = vbt.BBANDS.run(close, window=window, alpha=alpha).bbands.to_numpy()
    upper_band = bbands[:, 0]
    middle_band = bbands[:, 1]
    lower_band = bbands[:, 2]
    trend = np.where((lower_band < close < middle_band) | (close > upper_band), -1, trend if trend else 0)
    trend = np.where((middle_band < close < upper_band) | (close < lower_band), 1, trend)
    return trend


def add_atr_indicator(close: List[int], high: List[int], low: List[int], window: int = 14, trend = None):
    """Add an average true range indicator to the custom strategy"""

    atr = vbt.ATR.run(close, high=high, low=low, window=window).atr.to_numpy()
    trigger_price = close + atr
    entries = close.shift(-1)
    trend = np.where((entries > trigger_price), 1, trend if trend else 0)
    return trend


indicator_map = {
    'rsi': add_rsi_indicator,
    'ma': add_ma_indicator,
    'stoch': add_stoch_indicator,
    'bbands': add_bbands_indicator,
    'atr': add_atr_indicator
}

def custom_indicator(prices, ind_dict):
    """Creates a custom indicator by combining many indicators with different parameters"""

    trend = None
    for ind_type, inds in ind_dict.items():
        fn = indicator_map[ind_type]
        for ind in inds:
            inputs = [prices[input_name] for input_name in ind['inputs']] if len(ind['inputs']) > 1 else prices
            trend = fn(*inputs, **ind['params'], trend=trend)
            
    return trend

# shape of data
# {
#     'rsi': [
#         {
#               'inputs': ['Close'],
#               'params': {
#                   'entry': 80,
#                   'exit': 20,
#                   'window': 20
#               }
#         },
#     ]
# }

def run_strategy_handler(
    symbols: List[str],
    start_time: str,
    data: Dict[str, List[Dict]],
    end_time: str = datetime.datetime.now(),
    interval: str = '1m',
    class_name: str = 'Custom Indicator',
    output_names: List[str] = ['value'],
):
    """Use VectorBT's Indicator Factory API to construct a custom indicator/strategy"""

    input_names = ['close']

    if len(data['stoch']) > 0 or len(data['atr']) > 0:
        input_names.extend(['low', 'high'])

    ind = vbt.IndicatorFactory(
        class_name = class_name,
        input_names = input_names,
        param_names = ['ind_dict'],
        output_names = output_names
    ).from_apply_func(
        custom_indicator
    )

    prices = price_data(
        symbols=symbols,
        start_time=start_time,
        end_time=end_time,
        interval=interval,
        input_names=map(lambda s: s.capitalize(), input_names)
    )

    res = ind.run(
        prices,
        ind_dict=data
    )

    entries = res.value == 1.0
    exits = res.value == -1.0

    pf = vbt.Portfolio.from_signals(prices, entries, exits)

    return pf.total_returns()

symbols = ["TSLA"]
end_time = datetime.datetime.now()
start_time = end_time - datetime.timedelta(days=2)
data = {
    'rsi': [
        {
            'inputs': ['close'],
            'params': {
                'entry': 80,
                'exit': 20,
                'window': 20
            }
        },
    ],
    'ma': [
        {
            'inputs': ['close'],
            'params': {
                'window': 20
            },
        },
        {
            'inputs': ['close'],
            'params': {
                'window': 50
            },
        }
    ],
    'stoch': [],
    'bbands': [],
    'atr': [],
}

print(run_strategy_handler(symbols=symbols, start_time=start_time, data=data))