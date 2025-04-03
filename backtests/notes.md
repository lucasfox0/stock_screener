# Notes & Research Log

## Strategy Summary

- Modular app with sector-aware logic.
- Uses trailing P/E in **mean-reverting sectors**:
  - Energy, Utilities, Consumer Defensive, Financial Services
- Uses beta strategy in all **other sectors**:
  - BUY if beta < 0.9  
  - SELL if beta > 1.2  
  - HOLD otherwise
- Thresholds based on basic research — not yet validated.

---

## TODO (Short-Term)

- [ ] Backtest P/E strategy by sector  
- [ ] Backtest beta strategy on non-mean-reverting sectors  
- [ ] Log results in `backtests/log.csv`

---

## Backtest Plan – pe_sector_adjusted

- Trigger: Buy if trailing P/E < sector average  
- Sector: Energy  
- Universe: S&P 500 Energy stocks  
- Data: yfinance  
- Test period: Past 5 years (if available)  
- Rebalance: Monthly  
- Holding period: 30 days  
- Positioning: Equal-weighted, no leverage or shorting  
- Metrics: Sharpe ratio, average return, max drawdown

---

## Feedback

> “Value isn’t in printing metrics — it’s in simulating and logging performance.”  

> “P/E can punish growth stocks. Use forward P/E if possible — but great starting point.”  

> “Blend fundamentals and quant. Research factor models like Fama-French.”