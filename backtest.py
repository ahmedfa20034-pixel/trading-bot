#!/usr/bin/env python3
"""Backtesting Module"""

import json
import logging
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from src.mt5_client import MT5Client
from src.strategies import get_strategy
from src.risk_manager import RiskManager, TradeLogger

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


class Backtester:
    """Backtesting engine"""

    def __init__(self, config):
        self.config = config
        self.mt5 = MT5Client(config)
        self.risk_manager = RiskManager(config)
        self.trade_logger = TradeLogger()
        self.strategy = get_strategy(config["strategies"]["default"], config)
        self.trades = []

    def backtest_symbol(self, symbol, days=30):
        """Backtest on historical data"""
        logger.info(f"\nBacktesting {symbol} for last {days} days")

        if not self.mt5.connect():
            logger.error("Failed to connect to MT5")
            return None

        try:
            # Get historical data
            timeframe = self.config["trading"]["timeframe"]
            data = self.mt5.get_rates(symbol, timeframe, days * 24)

            if data is None or len(data) < 50:
                logger.warning(f"Insufficient data for {symbol}")
                return None

            initial_balance = 10000  # Starting balance for backtest
            current_balance = initial_balance
            trades_count = 0
            winning_trades = 0
            losing_trades = 0
            total_profit = 0

            # Simulate trades
            for i in range(50, len(data)):
                current_data = data.iloc[:i+1]
                signal = self.strategy.analyze(current_data)

                if signal["action"] != "HOLD":
                    entry_price = current_data["close"].iloc[-1]
                    next_price = data["close"].iloc[i+1] if i+1 < len(data) else entry_price

                    # Simulate trade outcome
                    if signal["action"] == "BUY":
                        profit = (next_price - entry_price) * 1.0
                    else:
                        profit = (entry_price - next_price) * 1.0

                    current_balance += profit
                    total_profit += profit
                    trades_count += 1

                    if profit > 0:
                        winning_trades += 1
                    else:
                        losing_trades += 1

                    trade_data = {
                        "timestamp": current_data["time"].iloc[-1],
                        "symbol": symbol,
                        "action": signal["action"],
                        "entry": entry_price,
                        "exit": next_price,
                        "profit": profit,
                        "reason": signal["reason"],
                    }
                    self.trades.append(trade_data)

            # Calculate statistics
            if trades_count > 0:
                win_rate = (winning_trades / trades_count) * 100
                avg_profit = total_profit / trades_count
                roi = (total_profit / initial_balance) * 100

                logger.info(f"\n{'='*50}")
                logger.info(f"Backtest Results for {symbol}")
                logger.info(f"{'='*50}")
                logger.info(f"Initial Balance: ${initial_balance:,.2f}")
                logger.info(f"Final Balance: ${current_balance:,.2f}")
                logger.info(f"Total Profit: ${total_profit:,.2f}")
                logger.info(f"ROI: {roi:.2f}%")
                logger.info(f"Total Trades: {trades_count}")
                logger.info(f"Winning Trades: {winning_trades}")
                logger.info(f"Losing Trades: {losing_trades}")
                logger.info(f"Win Rate: {win_rate:.2f}%")
                logger.info(f"Average Profit per Trade: ${avg_profit:.2f}")
                logger.info(f"{'='*50}\n")

                return {
                    "symbol": symbol,
                    "trades_count": trades_count,
                    "winning_trades": winning_trades,
                    "losing_trades": losing_trades,
                    "win_rate": win_rate,
                    "total_profit": total_profit,
                    "roi": roi,
                    "initial_balance": initial_balance,
                    "final_balance": current_balance,
                }
            else:
                logger.warning("No trades generated during backtest")
                return None

        finally:
            self.mt5.disconnect()

    def run(self):
        """Run backtest on all symbols"""
        logger.info("\n" + "="*50)
        logger.info("STARTING BACKTEST")
        logger.info("="*50)

        symbols = self.config["trading"]["symbols"]
        results = []

        for symbol in symbols:
            result = self.backtest_symbol(symbol, days=30)
            if result:
                results.append(result)

        # Summary
        if results:
            logger.info("\n" + "="*50)
            logger.info("BACKTEST SUMMARY")
            logger.info("="*50)
            total_trades = sum(r["trades_count"] for r in results)
            total_profit = sum(r["total_profit"] for r in results)
            avg_win_rate = sum(r["win_rate"] for r in results) / len(results)

            logger.info(f"Total Symbols Tested: {len(results)}")
            logger.info(f"Total Trades: {total_trades}")
            logger.info(f"Total Profit: ${total_profit:,.2f}")
            logger.info(f"Average Win Rate: {avg_win_rate:.2f}%")
            logger.info("="*50)


def main():
    """Main backtest function"""
    config_path = Path("config.json")
    if not config_path.exists():
        logger.error("config.json not found")
        return

    with open(config_path) as f:
        config = json.load(f)

    backtester = Backtester(config)
    backtester.run()


if __name__ == "__main__":
    main()
