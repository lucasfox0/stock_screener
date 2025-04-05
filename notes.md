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

## Current Strategy Plan

**Strategy:**  
Buy S&P 500 Energy stocks if trailing P/E < 16.71.  
Reevaluate portfolio **monthly**. Hold stocks if P/E < 16.71.  
Sell if P/E rises above the threshold.

**Entry Signal:**  
- Trailing P/E < 16.71  
- Check at the start of each month

**Exit Signal:**  
- Trailing P/E >= 16.71  
- Check monthly

**Rebalancing Frequency:**  
- Monthly (time-based, not P/E crossover)

**Universe:**  
- Energy sector stocks from the S&P 500  
- Will expand to broader Energy universe later

**Holding Period:**  
- Variable; depends on how long P/E stays below 16.71  
- Minimum 1 month

**Positioning:**  
- Equal weight per stock  
- Can enter same stock in multiple months if P/E stays below threshold

**Goal:**  
- Determine if P/E-based value screening outperforms a naive benchmark (e.g. equal-weighted Energy portfolio)

---

## Feedback

> “Value isn’t in printing metrics — it’s in simulating and logging performance.”  

> “P/E can punish growth stocks. Use forward P/E if possible — but great starting point.”  

> “Blend fundamentals and quant. Research factor models like Fama-French.”