# 📊 Strategies

This file documents the current strategies implemented in the stock screener. Each strategy includes its core logic, applicable sectors, and a short description.

---

## Strategy 1: `pe_sector_adjusted`

**Type**: Value Strategy (Mean-Reversion)  
**Logic**:
- For mean-reverting sectors:
  - **BUY** if P/E < sector average
  - **SELL** if P/E > 30
  - **HOLD** otherwise

**Applicable Sectors**:
- Consumer Defensive (avg P/E: 23.23)
- Utilities (avg P/E: 20.71)
- Financial Services (avg P/E: 18.01)
- Energy (avg P/E: 16.71)

**Notes**:
- These sectors are historically more stable and mean-reverting.
- This strategy assumes overvalued companies revert toward the sector’s average valuation.

---

## Strategy 2: `low_beta`

**Type**: Volatility Strategy (Low Volatility Anomaly)  
**Logic**:
- For non-mean-reverting sectors:
  - **BUY** if beta < 0.9
  - **SELL** if beta > 1.2
  - **HOLD** otherwise

**Applicable Sectors**:
- All sectors **except** Consumer Defensive, Utilities, Financial Services, and Energy

**Notes**:
- Based on academic findings that lower beta stocks often outperform on a risk-adjusted basis.
- Avoids high-beta names that may be overexposed to market drawdowns.
