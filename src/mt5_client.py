"""MetaTrader 5 Client Module"""

import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class MT5Client:
    """MetaTrader 5 Connection and Trading Client"""

    def __init__(self, config):
        """Initialize MT5 client"""
        self.config = config
        self.account = config["mt5"]["account"]
        self.password = config["mt5"]["password"]
        self.server = config["mt5"]["server"]
        self.connected = False

    def connect(self):
        """Connect to MT5"""
        try:
            if not mt5.initialize():
                logger.error("Failed to initialize MetaTrader5")
                return False

            if not mt5.login(self.account, self.password, self.server):
                logger.error(f"Login failed for account {self.account}")
                return False

            self.connected = True
            logger.info(f"Connected to MT5: {self.account}")
            return True
        except Exception as e:
            logger.error(f"MT5 connection error: {e}")
            return False

    def disconnect(self):
        """Disconnect from MT5"""
        if self.connected:
            mt5.shutdown()
            self.connected = False
            logger.info("Disconnected from MT5")

    def get_account_info(self):
        """Get account information"""
        try:
            account_info = mt5.account_info()
            if account_info:
                return {
                    "balance": account_info.balance,
                    "equity": account_info.equity,
                    "margin": account_info.margin,
                    "free_margin": account_info.margin_free,
                    "leverage": account_info.leverage,
                    "profit": account_info.profit,
                }
            return None
        except Exception as e:
            logger.error(f"Error getting account info: {e}")
            return None

    def get_rates(self, symbol, timeframe, count=100):
        """Get price data"""
        try:
            rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
            if rates is not None:
                df = pd.DataFrame(rates)
                df["time"] = pd.to_datetime(df["time"], unit="s")
                return df
            return None
        except Exception as e:
            logger.error(f"Error getting rates for {symbol}: {e}")
            return None

    def get_last_price(self, symbol):
        """Get current price"""
        try:
            tick = mt5.symbol_info_tick(symbol)
            if tick:
                return {
                    "ask": tick.ask,
                    "bid": tick.bid,
                    "last": tick.last,
                    "time": datetime.fromtimestamp(tick.time),
                }
            return None
        except Exception as e:
            logger.error(f"Error getting price for {symbol}: {e}")
            return None

    def send_order(self, symbol, order_type, volume, price, stop_loss, take_profit, comment=""):
        """Send trading order"""
        try:
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": volume,
                "type": order_type,
                "price": price,
                "sl": stop_loss,
                "tp": take_profit,
                "deviation": 20,
                "magic": 234000,
                "comment": comment,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

            result = mt5.order_send(request)
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                logger.error(f"Order failed: {result.comment}")
                return None

            logger.info(f"Order sent: {symbol} {order_type} {volume} lots")
            return result
        except Exception as e:
            logger.error(f"Error sending order: {e}")
            return None

    def buy(self, symbol, volume, price, stop_loss, take_profit, comment="BUY"):
        """Send buy order"""
        return self.send_order(
            symbol, mt5.ORDER_TYPE_BUY, volume, price, stop_loss, take_profit, comment
        )

    def sell(self, symbol, volume, price, stop_loss, take_profit, comment="SELL"):
        """Send sell order"""
        return self.send_order(
            symbol, mt5.ORDER_TYPE_SELL, volume, price, stop_loss, take_profit, comment
        )

    def get_positions(self, symbol=None):
        """Get open positions"""
        try:
            positions = mt5.positions_get(symbol=symbol)
            if positions:
                return pd.DataFrame(list(positions))
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error getting positions: {e}")
            return pd.DataFrame()

    def close_position(self, ticket):
        """Close position by ticket"""
        try:
            position = mt5.positions_get(ticket=ticket)[0]
            if position.type == mt5.ORDER_TYPE_BUY:
                order_type = mt5.ORDER_TYPE_SELL
            else:
                order_type = mt5.ORDER_TYPE_BUY

            price = mt5.symbol_info_tick(position.symbol).bid if order_type == mt5.ORDER_TYPE_SELL else mt5.symbol_info_tick(position.symbol).ask

            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": position.symbol,
                "volume": position.volume,
                "type": order_type,
                "price": price,
                "deviation": 20,
                "magic": 234000,
                "comment": "Close position",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

            result = mt5.order_send(request)
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                logger.info(f"Position {ticket} closed")
                return True
            return False
        except Exception as e:
            logger.error(f"Error closing position: {e}")
            return False
