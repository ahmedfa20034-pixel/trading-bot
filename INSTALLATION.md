# Installation Guide

## Prerequisites

- Python 3.8 or higher
- MetaTrader 5 installed on your system
- pip (Python package manager)
- Virtual environment (recommended)

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ahmedfa20034-pixel/trading-bot.git
cd trading-bot
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### 1. Update config.json

Edit `config.json` with your settings:

```json
{
  "mt5": {
    "account": "YOUR_ACCOUNT_NUMBER",
    "password": "YOUR_PASSWORD",
    "server": "YOUR_BROKER_SERVER"
  },
  "trading": {
    "symbols": ["EURUSD", "GBPUSD"],
    "timeframe": "H1",
    "risk_per_trade": 0.02
  },
  "notifications": {
    "email": {
      "enabled": true,
      "sender": "your_email@gmail.com",
      "password": "your_app_password"
    },
    "telegram": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "chat_id": "YOUR_CHAT_ID"
    }
  }
}
```

### 2. Create Logs Directory

```bash
mkdir -p logs
mkdir -p data
```

## Running the Bot

### Demo/Backtesting

Test your strategy with historical data:

```bash
python backtest.py
```

### Live Trading

**IMPORTANT: Always test on demo account first!**

```bash
python main.py
```

## Troubleshooting

### MetaTrader 5 Connection Issues

1. Make sure MetaTrader 5 is running
2. Verify account credentials
3. Check server name matches your broker
4. Ensure Python can access MT5 installation path

### Missing Dependencies

```bash
pip install --upgrade -r requirements.txt
```

### Permission Issues

```bash
# Grant execution permission (Linux/macOS)
chmod +x main.py backtest.py
```

## Next Steps

1. Test on a demo account
2. Review generated logs in `/logs` directory
3. Analyze backtest results
4. Adjust parameters as needed
5. Start with small positions on live account

## Support

For issues or questions, please open an issue on GitHub.
