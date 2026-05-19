# Forex & Binary Options Trading Bot

A fully automated trading bot for Forex and Binary Options using Python, MetaTrader 5, and advanced technical indicators.

## Features

✅ **Real-time Trading**
- Automated entry/exit signals
- Multi-timeframe analysis
- Multiple currency pairs support

✅ **Technical Indicators**
- Moving Average (SMA, EMA)
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands
- Stochastic Oscillator

✅ **Risk Management**
- Stop Loss management
- Take Profit settings
- Position sizing
- Risk-reward ratio calculations
- Maximum drawdown monitoring

✅ **Backtesting**
- Historical data analysis
- Strategy performance evaluation
- Win rate calculation
- Profit/Loss analysis

✅ **Monitoring & Alerts**
- Real-time trade notifications
- Email alerts
- Telegram notifications
- Trade logging

## Installation

### Requirements
- Python 3.8+
- MetaTrader 5
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/ahmedfa20034-pixel/trading-bot.git
cd trading-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

1. Edit `config.json` with your settings:

```json
{
  "mt5": {
    "account": "YOUR_ACCOUNT_NUMBER",
    "password": "YOUR_PASSWORD",
    "server": "YOUR_BROKER_SERVER"
  },
  "trading": {
    "symbols": ["EURUSD", "GBPUSD", "USDJPY"],
    "timeframe": "H1",
    "risk_per_trade": 0.02
  }
}
```

2. Update notification settings in `config.json`

## Usage

### Run Live Trading

```bash
python main.py
```

### Run Backtesting

```bash
python backtest.py
```

### Run with Specific Strategy

```bash
python main.py --strategy rsi_strategy --symbols EURUSD GBPUSD
```

## Project Structure

```
trading-bot/
├── main.py                 # Main bot runner
├── backtest.py            # Backtesting module
├── config.json            # Configuration file
├── requirements.txt       # Dependencies
├── src/
│   ├── __init__.py
│   ├── mt5_client.py      # MetaTrader 5 integration
│   ├── indicators.py      # Technical indicators
│   ├── strategies.py      # Trading strategies
│   ├── risk_manager.py    # Risk management
│   ├── trader.py          # Main trading logic
│   └── notifications.py   # Alert system
├── strategies/
│   ├── rsi_strategy.py
│   ├── macd_strategy.py
│   └── bollinger_strategy.py
├── logs/                  # Trade logs
└── data/                  # Historical data
```

## Strategies

### RSI Strategy
Buys when RSI < 30, sells when RSI > 70

### MACD Strategy
Buys on bullish crossover, sells on bearish crossover

### Bollinger Bands Strategy
Buys at lower band, sells at upper band

## Risk Management

- **Stop Loss**: Automatic exit on specified loss
- **Take Profit**: Automatic exit on specified profit
- **Position Sizing**: Based on account risk percentage
- **Drawdown Limit**: Stops trading if max drawdown exceeded

## Monitoring

The bot provides:
- Trade statistics
- Win/Loss ratio
- Profit factor
- Sharpe ratio
- Maximum drawdown

## Notifications

- Email alerts
- Telegram messages
- Trade log files

## Safety Features

⚠️ **IMPORTANT**
- Never trade with real money initially
- Test on demo account first
- Use stop loss on every trade
- Monitor the bot regularly
- Start with small position sizes

## Legal Disclaimer

This trading bot is provided for educational purposes only. Trading forex and binary options involves significant risk. Past performance does not guarantee future results. Always consult with a financial advisor before trading.

## Support & Contributing

For issues, questions, or contributions, please open an issue on GitHub.

## License

MIT License - See LICENSE file for details

---

**Made with ❤️ for traders**