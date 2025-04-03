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
- Filtering stocks based on current P/E
- Fetching historical price data
- Calculating returns
"""

def main():
    pe_threshold = 16.71

    # --- Get Energy Tickers ---
    # URL of Wikipedia page containing the list of S&P 500 companies
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    # Read first table from Wikipedia (S&P 500 company list)
    sp500_df = pd.read_html(url)[0]

    # Filter the DataFrame to include only rows where the sector is "Energy" and extract their ticker ("Symbol") as a list
    energy_tickers = sp500_df[sp500_df["GICS Sector"] == "Energy"]["Symbol"].tolist()


    # --- Create a List of Stocks with P/E Below Threshold ---
    buy_list = []

    # Loop through each ticker in energy_tickers and check the P/E value
    for ticker in tqdm(energy_tickers):
        try:
            info = yf.Ticker(ticker).info
            pe = info.get("trailingPE")
            if isinstance(pe, (int, float)) and pe < pe_threshold:
                buy_list.append(ticker)
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
    
    print(buy_list)


if __name__ == "__main__":
    main()