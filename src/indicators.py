"""Technical Indicators Module"""

import numpy as np
import pandas as pd
from typing import Tuple


class Indicators:
    """Technical indicators for trading analysis"""

    @staticmethod
    def sma(data, period=20):
        """Simple Moving Average"""
        return data["close"].rolling(window=period).mean()

    @staticmethod
    def ema(data, period=20):
        """Exponential Moving Average"""
        return data["close"].ewm(span=period, adjust=False).mean()

    @staticmethod
    def rsi(data, period=14):
        """Relative Strength Index"""
        close = data["close"]
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    @staticmethod
    def macd(data, fast=12, slow=26, signal=9):
        """MACD (Moving Average Convergence Divergence)"""
        close = data["close"]
        ema_fast = close.ewm(span=fast, adjust=False).mean()
        ema_slow = close.ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram

    @staticmethod
    def bollinger_bands(data, period=20, num_std=2):
        """Bollinger Bands"""
        sma = data["close"].rolling(window=period).mean()
        std = data["close"].rolling(window=period).std()
        upper_band = sma + (std * num_std)
        lower_band = sma - (std * num_std)
        return upper_band, sma, lower_band

    @staticmethod
    def stochastic(data, period=14, smooth_k=3, smooth_d=3):
        """Stochastic Oscillator"""
        low_min = data["low"].rolling(window=period).min()
        high_max = data["high"].rolling(window=period).max()
        k_percent = 100 * ((data["close"] - low_min) / (high_max - low_min))
        k_percent_smooth = k_percent.rolling(window=smooth_k).mean()
        d_percent = k_percent_smooth.rolling(window=smooth_d).mean()
        return k_percent_smooth, d_percent

    @staticmethod
    def atr(data, period=14):
        """Average True Range"""
        high_low = data["high"] - data["low"]
        high_close = abs(data["high"] - data["close"].shift())
        low_close = abs(data["low"] - data["close"].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        atr = true_range.rolling(window=period).mean()
        return atr

    @staticmethod
    def adx(data, period=14):
        """Average Directional Index"""
        high_diff = data["high"].diff()
        low_diff = -data["low"].diff()
        plus_dm = np.where((high_diff > low_diff) & (high_diff > 0), high_diff, 0)
        minus_dm = np.where((low_diff > high_diff) & (low_diff > 0), low_diff, 0)

        tr = Indicators.atr(data, period)
        plus_di = 100 * (pd.Series(plus_dm).rolling(window=period).mean() / tr)
        minus_di = 100 * (pd.Series(minus_dm).rolling(window=period).mean() / tr)
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = dx.rolling(window=period).mean()
        return adx, plus_di, minus_di

    @staticmethod
    def analyze_data(data, rsi_period=14, macd_params=(12, 26, 9), bb_period=20):
        """Comprehensive technical analysis"""
        analysis = {
            "rsi": Indicators.rsi(data, rsi_period).iloc[-1],
            "macd": Indicators.macd(data, *macd_params),
            "bb_upper": Indicators.bollinger_bands(data, bb_period)[0].iloc[-1],
            "bb_middle": Indicators.bollinger_bands(data, bb_period)[1].iloc[-1],
            "bb_lower": Indicators.bollinger_bands(data, bb_period)[2].iloc[-1],
            "sma": Indicators.sma(data, bb_period).iloc[-1],
            "ema": Indicators.ema(data, bb_period).iloc[-1],
        }
        return analysis
