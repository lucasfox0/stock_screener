## 2025-04-12

Currently trying to scrape with a while loop to run through all failed tickers over and over again. Might just want to try buying proxies. I implemented the failed ticker while loop myself but it defenitly needs to be refactored, preferably into one loop.

It's hard to write a TODO because I just need to get this EPS data scraped and other things keep coming up while doing that.

So today I want to refactor my loop and add meta data to my JSON to potentially help in the future.

---

## 2025-04-11

Still trying to prevent being flagged. Going to add a longer timer and if that doesn't work I'll do something else.

Starting to get a little too vibe codey... git restored to yesterday and going to start over tomorrow.

The issue I'm running into is that I am being captchaed about half way through even with an aritrary delay and different browsers. I plan to fix this by just getting through as much as I can, then looping through the "failed tickers" over and over until I do not get captchaed.

TODO:
- Review code
- Add different browsers
- Longer delay
- Make a list of failed that either are saved to JSON or get looped immediately after

The code is making sense now. We just need to try browssers and longer delay. Then try stuff with failed list. I DONT NEED LLM FOR THIS.

---

## 2025-04-10

All I did was remove redundant comments and started looping through tickers.

Got flagged so we need to add proxies and randomness.

---

## 2025-04-08

Finished error handling and modularizing. Also added a function to get a url from any ticker so it isn't hardcoded. I added comments to every line in my code to ensure I understand it. Eventually I'd like to try and build it again from scratch. 

Tomorrow: update requirements.txt, error handling incase of issue w/ url, remove the clarification comments, get EPS data for all tickers

---

## 2025-04-07

All I did was delete a couple print statements. So tired. Refactor more tomorrow.

---

## 2025-04-06

Pulled EPS data from MacroTrends. Still need to refactor code by adding/deleting lines and adding error handling.

---

## 2025-04-05

My next steps are to find a place that offers historical P/E data (or just EPS data) so I can start a real backtest.

---

## 2025-04-02

I finished my demo backtest:
- Scraped energy tickers in the S&P 500 from Wikipedia
- Pulled today's P/E ratios using yfinance
- Built a buy list for stocks with P/E < 16.71
- Pulled historical price data for those tickers
- Calculated 1 year return = (todays_price - year_ago_price) / year_ago_price
- Printed results and overall winrate and average return

Didn't log this because it wasn't a real strategy or even backtest.
This was more so just practice getting historical data and scraping.

---

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

