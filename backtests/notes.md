# 🧠 Notes & Research Log

## Thought Process

- The app is now modular and prints clean, sector-aware recommendations.
- P/E strategy is used **only in mean-reverting sectors**:
  - Energy
  - Utilities
  - Consumer Defensive
  - Financial Services
- Beta strategy is used for all **non-mean-reverting sectors**:
  - **BUY** if beta < 0.9
  - **SELL** if beta > 1.2
  - **HOLD** otherwise
- Thresholds are based on general research, not yet backtested.
- Using **trailing P/E** due to free data limitations.
- Sector P/E averages were pulled from ChatGPT-generated tables and need to be backtested.

---

## ❓ Questions to Figure Out

- Where can I get **forward P/E** or forward earnings estimates for free?
- Do beta thresholds (0.9/1.2) work across different time periods and universes?
- What’s the ideal **rebalancing frequency** (daily, monthly, quarterly)?
- Should I **re-enter** a stock if it flips from SELL → BUY later?
- Can I combine P/E and beta into a single signal in the future?

---

## ✅ TODO (Short-Term)

- [ ] Backtest P/E strategy by sector
- [ ] Backtest beta strategy on non-mean-reverting sectors
- [ ] Log results in `backtests/log.csv`

---

## 🧪 Backtest Design Ideas

- **Universe**: Top ~100 stocks by market cap
- **Test period**: 3–5 years (to smooth out noise)
- **Frequency**: Monthly rebalance
- **Entry signal**: BUY
- **Exit signal**: SELL or after N months
- **HOLD** means hold position

### Backtest Plan - pe_sector_adjusted (Energy)

- Strategy: Buy if trailing P/E < 16.71 (sector average)
- Sector: Energy
- Universe: Only Energy stock from the S&P 500
- Data source: yfinance
- Test window: Past 5 years (or whatever is available)
- Holding period: 30 days
- Rebalancing frequency: Monthly
- Positioning: Equal-weighted portfolio
- No leverage, no shorting, no stop-loss
- Evaluation: Sharpe ratio, average return, max drawdown

---

## 📣 Feedback from Friends

> "Combine fundamentals with quant. Read about Fama-French factors"

> “Just printing metrics is a start — but value comes from what you **do** with the data. Simulate strategies, quantify performance, and log results.”

> “Trailing P/E isn’t ideal — growth stocks will look expensive. Try to use **forward P/E** if you can. But this is a solid foundation.”