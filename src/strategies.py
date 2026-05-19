"""Trading Strategies Module"""

import logging
from src.indicators import Indicators

logger = logging.getLogger(__name__)


class TradingStrategy:
    """Base trading strategy class"""

    def __init__(self, config):
        self.config = config
        self.indicators = Indicators()

    def analyze(self, data):
        """Analyze and generate signals"""
        raise NotImplementedError


class RSIStrategy(TradingStrategy):
    """RSI-based trading strategy"""

    def __init__(self, config):
        super().__init__(config)
        self.oversold = config["strategies"]["rsi"]["oversold"]
        self.overbought = config["strategies"]["rsi"]["overbought"]
        self.period = config["strategies"]["rsi"]["period"]

    def analyze(self, data):
        """RSI analysis"""
        rsi = Indicators.rsi(data, self.period)
        current_rsi = rsi.iloc[-1]

        signal = {
            "action": "HOLD",
            "confidence": 0,
            "reason": "",
        }

        if current_rsi < self.oversold:
            signal["action"] = "BUY"
            signal["confidence"] = (self.oversold - current_rsi) / self.oversold
            signal["reason"] = f"RSI {current_rsi:.2f} < {self.oversold} (Oversold)"
        elif current_rsi > self.overbought:
            signal["action"] = "SELL"
            signal["confidence"] = (current_rsi - self.overbought) / (100 - self.overbought)
            signal["reason"] = f"RSI {current_rsi:.2f} > {self.overbought} (Overbought)"

        return signal


class MACDStrategy(TradingStrategy):
    """MACD-based trading strategy"""

    def __init__(self, config):
        super().__init__(config)
        self.fast = config["strategies"]["macd"]["fast"]
        self.slow = config["strategies"]["macd"]["slow"]
        self.signal = config["strategies"]["macd"]["signal"]

    def analyze(self, data):
        """MACD analysis"""
        macd_line, signal_line, histogram = Indicators.macd(
            data, self.fast, self.slow, self.signal
        )

        signal = {
            "action": "HOLD",
            "confidence": 0,
            "reason": "",
        }

        current_macd = macd_line.iloc[-1]
        current_signal = signal_line.iloc[-1]
        prev_macd = macd_line.iloc[-2]
        prev_signal = signal_line.iloc[-2]

        # Bullish crossover
        if prev_macd < prev_signal and current_macd > current_signal:
            signal["action"] = "BUY"
            signal["confidence"] = 0.8
            signal["reason"] = "Bullish MACD crossover"
        # Bearish crossover
        elif prev_macd > prev_signal and current_macd < current_signal:
            signal["action"] = "SELL"
            signal["confidence"] = 0.8
            signal["reason"] = "Bearish MACD crossover"

        return signal


class BollingerBandsStrategy(TradingStrategy):
    """Bollinger Bands-based trading strategy"""

    def __init__(self, config):
        super().__init__(config)
        self.period = config["strategies"]["bollinger"]["period"]
        self.std_dev = config["strategies"]["bollinger"]["std_dev"]

    def analyze(self, data):
        """Bollinger Bands analysis"""
        upper, middle, lower = Indicators.bollinger_bands(
            data, self.period, self.std_dev
        )

        signal = {
            "action": "HOLD",
            "confidence": 0,
            "reason": "",
        }

        current_price = data["close"].iloc[-1]
        current_lower = lower.iloc[-1]
        current_upper = upper.iloc[-1]
        current_middle = middle.iloc[-1]

        # Price at lower band
        if current_price <= current_lower:
            signal["action"] = "BUY"
            signal["confidence"] = 0.7
            signal["reason"] = f"Price {current_price:.4f} at lower band {current_lower:.4f}"
        # Price at upper band
        elif current_price >= current_upper:
            signal["action"] = "SELL"
            signal["confidence"] = 0.7
            signal["reason"] = f"Price {current_price:.4f} at upper band {current_upper:.4f}"

        return signal


class CombinedStrategy(TradingStrategy):
    """Combined multi-indicator strategy"""

    def __init__(self, config):
        super().__init__(config)
        self.rsi_strategy = RSIStrategy(config)
        self.macd_strategy = MACDStrategy(config)
        self.bb_strategy = BollingerBandsStrategy(config)

    def analyze(self, data):
        """Combined analysis from multiple strategies"""
        rsi_signal = self.rsi_strategy.analyze(data)
        macd_signal = self.macd_strategy.analyze(data)
        bb_signal = self.bb_strategy.analyze(data)

        # Count signals
        buy_count = sum(
            1
            for s in [rsi_signal, macd_signal, bb_signal]
            if s["action"] == "BUY"
        )
        sell_count = sum(
            1
            for s in [rsi_signal, macd_signal, bb_signal]
            if s["action"] == "SELL"
        )

        signal = {
            "action": "HOLD",
            "confidence": 0,
            "reason": "",
            "indicators": {
                "rsi": rsi_signal,
                "macd": macd_signal,
                "bb": bb_signal,
            },
        }

        # Require at least 2 signals
        if buy_count >= 2:
            signal["action"] = "BUY"
            signal["confidence"] = min(buy_count / 3, 1.0)
            signal["reason"] = f"Combined signal: {buy_count} indicators bullish"
        elif sell_count >= 2:
            signal["action"] = "SELL"
            signal["confidence"] = min(sell_count / 3, 1.0)
            signal["reason"] = f"Combined signal: {sell_count} indicators bearish"

        return signal


def get_strategy(strategy_name, config):
    """Factory function to get strategy instance"""
    strategies = {
        "rsi_strategy": RSIStrategy,
        "macd_strategy": MACDStrategy,
        "bollinger_strategy": BollingerBandsStrategy,
        "combined_strategy": CombinedStrategy,
    }

    strategy_class = strategies.get(strategy_name, CombinedStrategy)
    return strategy_class(config)
