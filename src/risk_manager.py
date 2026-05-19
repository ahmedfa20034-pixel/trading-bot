"""Risk Management Module"""

import logging
from decimal import Decimal

logger = logging.getLogger(__name__)


class RiskManager:
    """Position sizing and risk management"""

    def __init__(self, config):
        self.config = config
        self.risk_per_trade = config["trading"]["risk_per_trade"]
        self.max_positions = config["trading"]["max_positions"]
        self.max_drawdown = config["trading"]["max_drawdown"]

    def calculate_position_size(self, account_balance, stop_loss_pips, pip_value):
        """Calculate position size based on risk"""
        try:
            risk_amount = account_balance * self.risk_per_trade
            stop_loss_amount = stop_loss_pips * pip_value
            position_size = risk_amount / stop_loss_amount
            return max(0.01, round(position_size, 2))
        except Exception as e:
            logger.error(f"Error calculating position size: {e}")
            return 0.01

    def check_drawdown(self, initial_balance, current_equity):
        """Check if max drawdown exceeded"""
        if initial_balance == 0:
            return False

        drawdown = (initial_balance - current_equity) / initial_balance
        if drawdown > self.max_drawdown:
            logger.warning(
                f"Max drawdown exceeded: {drawdown:.2%} > {self.max_drawdown:.2%}"
            )
            return True
        return False

    def can_open_position(self, open_positions_count):
        """Check if we can open new position"""
        return open_positions_count < self.max_positions

    def calculate_sl_tp(self, entry_price, direction, stop_loss_pips, take_profit_pips):
        """Calculate stop loss and take profit prices"""
        pip_move = 0.0001  # For most pairs

        if direction == "BUY":
            stop_loss = entry_price - (stop_loss_pips * pip_move)
            take_profit = entry_price + (take_profit_pips * pip_move)
        else:  # SELL
            stop_loss = entry_price + (stop_loss_pips * pip_move)
            take_profit = entry_price - (take_profit_pips * pip_move)

        return round(stop_loss, 5), round(take_profit, 5)

    def calculate_reward_risk_ratio(self, entry_price, stop_loss, take_profit, direction):
        """Calculate reward to risk ratio"""
        if direction == "BUY":
            risk = entry_price - stop_loss
            reward = take_profit - entry_price
        else:
            risk = stop_loss - entry_price
            reward = entry_price - take_profit

        if risk == 0:
            return 0
        return reward / risk


class TradeLogger:
    """Log and track trades"""

    def __init__(self, filename="logs/trades.csv"):
        self.filename = filename
        self.trades = []

    def add_trade(self, trade_data):
        """Add trade entry"""
        self.trades.append(trade_data)
        logger.info(f"Trade logged: {trade_data}")

    def get_statistics(self):
        """Calculate trading statistics"""
        if not self.trades:
            return {}

        total_trades = len(self.trades)
        winning_trades = sum(1 for t in self.trades if t.get("profit", 0) > 0)
        losing_trades = total_trades - winning_trades
        total_profit = sum(t.get("profit", 0) for t in self.trades)
        average_profit = total_profit / total_trades if total_trades > 0 else 0

        stats = {
            "total_trades": total_trades,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "win_rate": (winning_trades / total_trades * 100) if total_trades > 0 else 0,
            "total_profit": total_profit,
            "average_profit": average_profit,
            "profit_factor": (
                sum(t.get("profit", 0) for t in self.trades if t.get("profit", 0) > 0)
                / abs(sum(t.get("profit", 0) for t in self.trades if t.get("profit", 0) < 0))
                if any(t.get("profit", 0) < 0 for t in self.trades)
                else 0
            ),
        }
        return stats
