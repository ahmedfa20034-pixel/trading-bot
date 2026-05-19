# Trading Strategies Documentation

## Available Strategies

### 1. RSI Strategy (Relative Strength Index)

**How it works:**
- Buys when RSI < 30 (oversold condition)
- Sells when RSI > 70 (overbought condition)

**Configuration:**
```json
"rsi": {
  "period": 14,
  "oversold": 30,
  "overbought": 70
}
```

**Best for:**
- Range-bound markets
- Identifying overbought/oversold conditions

**Risk:** Can give false signals in trending markets

---

### 2. MACD Strategy (Moving Average Convergence Divergence)

**How it works:**
- Generates BUY signal on bullish crossover (MACD > Signal line)
- Generates SELL signal on bearish crossover (MACD < Signal line)

**Configuration:**
```json
"macd": {
  "fast": 12,
  "slow": 26,
  "signal": 9
}
```

**Best for:**
- Trending markets
- Momentum identification

**Risk:** Slower response to quick market changes

---

### 3. Bollinger Bands Strategy

**How it works:**
- Buys when price touches lower band
- Sells when price touches upper band

**Configuration:**
```json
"bollinger": {
  "period": 20,
  "std_dev": 2
}
```

**Best for:**
- Volatility-based trading
- Mean reversion trades

**Risk:** Can lead to whipsaws in highly volatile markets

---

### 4. Combined Strategy

**How it works:**
- Uses signals from RSI, MACD, and Bollinger Bands
- Requires at least 2 indicators to agree
- Reduces false signals

**Best for:**
- General market conditions
- Conservative traders

**Advantage:** Better signal quality with reduced false signals

---

## Selecting a Strategy

1. **For Beginners:** Start with Combined Strategy
2. **For Range-bound Markets:** Use RSI Strategy
3. **For Trending Markets:** Use MACD Strategy
4. **For Volatile Markets:** Use Bollinger Bands

## Customizing Strategies

Edit `config.json` to switch strategies:

```json
"strategies": {
  "default": "rsi_strategy"  // Change this
}
```

Options:
- `rsi_strategy`
- `macd_strategy`
- `bollinger_strategy`
- `combined_strategy`

## Testing Strategies

Always backtest before live trading:

```bash
python backtest.py
```

Check the logs for:
- Win rate percentage
- Profit factor
- Maximum drawdown
- Total profit/loss
