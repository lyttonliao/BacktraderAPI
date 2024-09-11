import vectorbt as vbt
import pandas as pd
import numpy as np
import datetime

from typing import Optional, Any, Dict, List


def price_data(
    symbols: List[str], 
    start_time: str, 
    end_time: str = datetime.datetime.now(), 
    interval: str = "1m",
    input_type: str = "Close"
):
    """Downloads data Yahoo Finance through VectorBT's API"""
    data = vbt.YFData.download(
        symbols=symbols,
        start=start_time,
        end=end_time,
        missing_index='drop',
        interval=interval).get(input_type)
    
    return data


def custom_indicator(*params: List[Dict]):
    """Creates a custom indicator by combining many indicators with different parameters"""
    pass


def add_rsi_indicator(close: List[int], window: int, entry: int = 20, exit: int = 80):
    """Add a relative strength index indicator to the custom strategy"""

    rsi = vbt.RSI.run(close, window=window).rsi.to_numpy()
    trend = np.where(rsi > exit, -1, 0)
    trend = np.where(rsi < entry, 1, trend)
    return trend


def add_ma_indicator(close: List[int], window: int):
    "Add a moving average index indicator to the custom strategy"

    ma = vbt.MA.run(close, window=window).ma.to_numpy()
    trend = np.where(close < ma, 1, 0)
    return trend


def add_stoch_indicator(close: List[int], high: List[int], low: List[int], k_window: int, d_window, entry: int = 20, exit: int = 80):
    """Add a stochastic oscillator indicator to the custom strategy"""

    stoch = vbt.STOCH.run(close, high=high, low=low, k_window=k_window, d_window=d_window).stoch.to_numpy()
    trend = np.where(stoch > exit, -1, 0)
    trend = np.where(stoch < entry, 1, trend)
    return trend


def add_bbands_indicator(close: List[int], window: int = 20, alpha: int = 2):
    """Add a bollinger bands indicator to the custom strategy, currently supports basic bollinger actions, does not trace contraction or expansion of the bands"""

    bbands = vbt.BBANDS.run(close, window=window, alpha=alpha).bbands.to_numpy()
    upper_band = bbands[:, 0]
    middle_band = bbands[:, 1]
    lower_band = bbands[:, 2]
    trend = np.where( (lower_band < close < middle_band) | (close > upper_band), -1, 0)
    trend = np.where( (middle_band < close < upper_band) | (close < lower_band), 1, trend)
    return trend


def add_atr_indicator(close: List[int], high: List[int], low: List[int], window: int = 14):
    """Add an average true range indicator to the custom strategy"""

    atr = vbt.ATR.run(close, high=high, low=low, window=window).atr.to_numpy()
    trigger_price = close + atr
    entries = close.shift(-1)
    trend = np.where( (entries > trigger_price), 1, 0)
    return trend

    