# **Monthly P/E-Based Strategy**
---
### **Goal**: 
Implement a simple, fundamental-based backtestable strategy using P/E ratios for mean-reverting sectors, starting with Energy. Focusing on code quality and clarity, with potential to use across other sectors. 

---
### **Thesis**:
In mean-reverting sectors like Energy, valuation tends to oscillate around a long-term average. By comparing each stock's historical quarterly P/E to its sector average, we can identify relative under/overvaluation. 
- **Buy**: stocks with a P/E below sector average
- **Sell**: stocks with a P/E above sector average
- **Rebalance**: monthly
---
### **Implementation Steps**:
1. Fetch monthly closing prices from 2015-current
2. Fetch quarterly EPS from 2015-current
3. Calculate monthly P/E
4. Determine sector average P/E (quarterly)
5. Rebalance monthly
6. Backtest over multiple years
7. Record performance metrics
	* Sharpe ratio
	* Max drawdown
	* CAGR
	* Win rate 
	* Volatility
