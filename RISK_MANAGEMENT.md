# Risk Management Guide

## Key Risk Management Principles

### 1. Position Sizing

**Formula:**
```
Position Size = (Account Risk Amount) / (Stop Loss in Pips × Pip Value)
```

**Example:**
- Account: $10,000
- Risk per trade: 2% = $200
- Stop Loss: 50 pips
- Position Size = $200 / (50 × $0.0001) = 4.0 lots

**Configuration:**
```json
"trading": {
  "risk_per_trade": 0.02  // 2% of account
}
```

### 2. Stop Loss (SL) and Take Profit (TP)

**Configuration:**
```json
"risk_management": {
  "stop_loss_pips": 50,
  "take_profit_pips": 100,
  "trailing_stop": true,
  "trailing_step": 20
}
```

**Reward-to-Risk Ratio:**
- TP (100) / SL (50) = 2:1 (Good)
- Aim for minimum 1.5:1 ratio
- Better strategies have 2:1 or higher

### 3. Maximum Positions

**Limit concurrent trades:**
```json
"trading": {
  "max_positions": 5  // Max 5 open positions
}
```

**Benefits:**
- Reduces correlation risk
- Prevents over-leverage
- Easier to manage

### 4. Maximum Drawdown

**Definition:** Maximum peak-to-trough decline

**Configuration:**
```json
"trading": {
  "max_drawdown": 0.15  // Stop if 15% drawdown
}
```

**When to set:**
- Conservative: 10%
- Moderate: 15%
- Aggressive: 20-25%

## Risk Management Checklist

- ☐ Never trade without Stop Loss
- ☐ Risk only 1-2% per trade
- ☐ Maintain 1.5:1+ reward-to-risk ratio
- ☐ Limit maximum concurrent positions
- ☐ Monitor drawdown daily
- ☐ Keep trading journal
- ☐ Review performance weekly
- ☐ Adjust position size with account growth

## Example Risk Scenario

**Account:** $10,000
**Strategy:** Risk 2% per trade

| Trade | Entry | SL | TP | Risk | Potential Reward | Status |
|-------|-------|----|----|------|------------------|---------|
| 1 | 1.1050 | 1.1000 | 1.1150 | $200 | $400 | +$400 |
| 2 | 1.1150 | 1.1100 | 1.1300 | $200 | $400 | -$200 |
| 3 | 1.1200 | 1.1150 | 1.1350 | $200 | $400 | +$400 |
| **Total** | - | - | - | **$600** | **$800** | **+$600** |

## Account Growth Strategy

1. **Month 1-2:** Build confidence, focus on risk management
2. **Month 3-6:** Once strategy is profitable, increase position size by 10-20%
3. **Ongoing:** Scale up gradually as account grows

**DON'T:** Increase position size after losses
**DO:** Adjust based on account equity

## Warning Signs

⚠️ **Stop trading if:**
- 3 consecutive losses
- Drawdown reaches max_drawdown limit
- Strategy performance drops significantly
- You feel emotional about trading
- Market conditions change drastically

Take a break, analyze, and adjust before resuming.
