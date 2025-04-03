import yfinance as yf
import pandas as pd
from tqdm import tqdm

"""
Strategy:
- Look at today's P/E for each energy stock.
- If the P/E is below 16.71, the strategy would have signaled a BUY.
- Then go back one year and get the price from then.
- Calculate the return: (today_price - year_ago_price) / year_ago_price.
- A positive return suggests the signal may have been effective.

NOTE: THIS IS NOT A VALID BACKTEST.
This is simply for building skills in:
- Filtering stocks based on fundamentals
- Fetching historical price data
- Calculating returns
"""

def main():
    """
    Executes a mock P/E strategy to evaluate energy stocks in the S&P 500.
    """

    pe_threshold = 16.71

    # --- Get Energy Tickers ---
    # URL of Wikipedia page containing the list of S&P 500 companies
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    # Read first table from Wikipedia (S&P 500 company list)
    sp500_df = pd.read_html(url)[0]

    # Filter the DataFrame to include only rows where the sector is "Energy" and extract their ticker ("Symbol") as a list
    energy_tickers = sp500_df[sp500_df["GICS Sector"] == "Energy"]["Symbol"].tolist()

    # Loop through each ticker in energy_tickers and check the P/E value to create buy list
    buy_list = []
    for ticker in tqdm(energy_tickers):
        try:
            info = yf.Ticker(ticker).info
            pe = info.get("trailingPE")
            if isinstance(pe, (int, float)) and pe < pe_threshold:
                buy_list.append(ticker)
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
    
    # Loop through each ticker in the buy list and get today's price and last year's price
    price_dict = {}
    for ticker in tqdm(buy_list):
        try:
            hist = yf.Ticker(ticker).history(period="1y") # Get DataFrame from past year
            todays_price =  info.iloc[-1]["Close"]
            last_years_price = info.iloc[0]["Close"]

            price_dict[ticker] = {
            "todays_price": float(todays_price),
            "year_ago_price": float(last_years_price)
            }
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")

    # --- Calculate return ---
    returns = {}

    for ticker, prices in price_dict.items():
        today = prices["todays_price"]
        year_ago = prices["year_ago_price"]
        pct_return = (today - year_ago) / year_ago
        returns[ticker] = pct_return
        print(f"{ticker}: {pct_return:.2%}")

    # Print backtest results
    print("\n--- Backtest Summary ---")

    total_return = sum(returns.values())
    num_stocks = len(returns)
    avg_return = total_return / num_stocks if num_stocks > 0 else 0
    positive_returns = sum(1 for r in returns.values() if r > 0)
    win_rate = (positive_returns / num_stocks) * 100 if num_stocks > 0 else 0

    print(f"Number of Stocks: {num_stocks}")
    print(f"Average Return:   {avg_return:.2%}")
    print(f"Win Rate:         {win_rate:.2f}%")

    print("\nScript completed.\n")


if __name__ == "__main__":
    main()