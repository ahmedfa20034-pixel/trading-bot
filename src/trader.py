"""Main Trading Engine"""

import logging
import time
from datetime import datetime
from src.mt5_client import MT5Client
from src.strategies import get_strategy
from src.risk_manager import RiskManager, TradeLogger
from src.notifications import NotificationManager

logger = logging.getLogger(__name__)


class TradingEngine:
    """Main trading engine"""

    def __init__(self, config):
        self.config = config
        self.mt5 = MT5Client(config)
        self.risk_manager = RiskManager(config)
        self.notification_manager = NotificationManager(config)
        self.trade_logger = TradeLogger()
        self.strategy = get_strategy(config["strategies"]["default"], config)
        self.running = False

    def start(self):
        """Start trading engine"""
        if not self.mt5.connect():
            logger.error("Failed to connect to MT5")
            return False

        self.running = True
        logger.info("Trading engine started")
        return True

    def stop(self):
        """Stop trading engine"""
        self.running = False
        self.mt5.disconnect()
        logger.info("Trading engine stopped")

    def process_signal(self, signal, symbol, account_info):
        """Process trading signal"""
        if signal["action"] == "HOLD":
            return None

        # Check if we can open new position
        positions = self.mt5.get_positions(symbol)
        if not self.risk_manager.can_open_position(len(positions)):
            logger.warning(f"Max positions reached for {symbol}")
            return None

        # Get current price
        price_info = self.mt5.get_last_price(symbol)
        if not price_info:
            return None

        entry_price = price_info["ask"] if signal["action"] == "BUY" else price_info["bid"]

        # Calculate stop loss and take profit
        stop_loss_pips = self.config["risk_management"]["stop_loss_pips"]
        take_profit_pips = self.config["risk_management"]["take_profit_pips"]

        sl, tp = self.risk_manager.calculate_sl_tp(
            entry_price, signal["action"], stop_loss_pips, take_profit_pips
        )

        # Calculate position size
        volume = self.risk_manager.calculate_position_size(
            account_info["balance"], stop_loss_pips, 0.0001
        )

        # Execute trade
        if signal["action"] == "BUY":
            result = self.mt5.buy(symbol, volume, entry_price, sl, tp, signal["reason"])
        else:
            result = self.mt5.sell(symbol, volume, entry_price, sl, tp, signal["reason"])

        if result:
            # Log trade
            trade_data = {
                "timestamp": datetime.now(),
                "symbol": symbol,
                "action": signal["action"],
                "entry_price": entry_price,
                "stop_loss": sl,
                "take_profit": tp,
                "volume": volume,
                "reason": signal["reason"],
                "ticket": result.order,
            }
            self.trade_logger.add_trade(trade_data)

            # Send notification
            message = f"Trade opened: {signal['action']} {symbol} {volume} lots @ {entry_price}"
            self.notification_manager.send_notification(
                "Trade Alert", message, signal["reason"]
            )

            return trade_data
        return None

    def scan_market(self):
        """Scan all configured symbols for trading signals"""
        symbols = self.config["trading"]["symbols"]
        timeframe = self.config["trading"]["timeframe"]
        account_info = self.mt5.get_account_info()

        if not account_info:
            logger.error("Could not get account info")
            return

        for symbol in symbols:
            try:
                # Get price data
                data = self.mt5.get_rates(symbol, timeframe, 100)
                if data is None or len(data) < 50:
                    logger.warning(f"Insufficient data for {symbol}")
                    continue

                # Analyze with strategy
                signal = self.strategy.analyze(data)

                if signal["action"] != "HOLD":
                    logger.info(f"{symbol}: {signal['action']} - {signal['reason']}")
                    self.process_signal(signal, symbol, account_info)

            except Exception as e:
                logger.error(f"Error processing {symbol}: {e}")
                continue

    def run(self, interval=60):
        """Main trading loop"""
        if not self.start():
            return

        try:
            while self.running:
                logger.info("Scanning market...")
                self.scan_market()
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("Received interrupt signal")
        finally:
            self.stop()
            stats = self.trade_logger.get_statistics()
            logger.info(f"Trading Statistics: {stats}")
