# FMP Legacy V1 API Strategy Notes
Base URL: https://financialmodelingprep.com/api/
## Strategy Thesis

### Mean-Reverting Sectors
- **Buy** when a stock’s **P/E ratio** is significantly **below** its sector average.
- **Sell** when the P/E ratio **reverts to or rises above** the sector average.

---

## Data Requirements
- Tickers in a specific sector
- 5+ year historical P/E for the tickers
	- If P/E is unavailable then need EPS and price from past 5+ years

---

## Potentially Helpful Endpoints 

| Name                   | Endpoint                                           | Notes                                                                                                                     | Example Return                                                                                                                                            |
| ---------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Company Profile        | `/v3/profile/AAPL`                                 | Returns very generic _current_ information on a company, including beta.                                                  | [{"beta": 1.259}]                                                                                                                                         |
| Screener (Stock)       | `/v3/stock-screener`                               | Returns a list of stocks based on specific criteria such as a specific beta, dividend, sector, and more.                  | [ { "symbol": "BAC-PL",...}]                                                                                                                              |
| Stock Grade            | `/v3/grade/{ticker}`                               | Returns a list of ratings provided by different hedge funds, investment firms, and analysts. May be useful in the future. | [{"previousGrade": "Buy",<br>    "newGrade": "Buy"}]                                                                                                      |
| Analyst Recommendation | `/v3/analyst-stock-recommendations/{ticker}`       | Similar to `Stock Grade`, this gives a monthly recommendation on hold/sell/buy, including previous recommendations.       | [{"analystRatingsStrongBuy": 8}]                                                                                                                          |
| Company Outlook        | `/v4/company-outlook?symbol={ticker}`              | Gives a very in-depth overview of a company (about 600 lines)                                                             | price, beta, average volume, market cap, range, executives, address, ratios, metrics, inside trades, split history, news, rating, annual financials, etc. |
| Key Metrics            | `/v3/key-metrics/{ticker}?period={annual/quarter}` | Gives a much more concise overview of metrics.                                                                            | Gives historical P/E.                                                                                                                                     |
| Ratios                 | `/v3/ratios/{ticker}?period={annual/quarter}`      | Similar `Key Metrics` but gives soley ratios including P/E.                                                               |                                                                                                                                                           |



