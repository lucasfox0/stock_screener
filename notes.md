## 2025-04-01

**Current Status:**
- Refactored logic into separate functions.

**Next Steps:**
- Start first backtest to see the effectiveness of strategies.

---

## 2025-03-31

**Current Status:**
- Gives basic metrics and recommends either BUY/HOLD/SELL based on sector, then P/E or beta.

**Next Steps:**
- Refactor code into more functions.
- Start first backtest.

---

## 2025-03-29

All that's left for MVP is giving a super basic buy/sell/hold recommendation.
- Then I can add way more in-depth recommendations.
- Recommend based off P/E & dividend yeild for MVP:
* P/E ratio is below industry average AND dividend yield is above 1% (BUY)
* P/E ratio is above 30 (SELL)
* else (HOLD)

**Tomorrow:**
- Finish MVP
- Research how to make it "useful"

---

## 2025-03-28

Input: AAPL
Output:
  Ticker: AAPL
  Company: Apple Inc.
  Price: $174.50
  PE Ratio: 28.4
  Dividend Yield: 0.55%
  Market Cap: $2.7T
  52-Week-High: $199.62
  52-Week-Low: $123.45

  Is PE Ratio above industry average? Yes
  Is Dividend Yield above 1%? No
  Recommendation: HOLD

1. Buy low P/E and sell high P/E
2. See what industries this works best in
3. Combine fundamentals w/ quant
4. Buy low beta, sell high beta

