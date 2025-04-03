import pandas as pd

def main():
    # Step 1: Scrape list of Energy sector stocks from the S&P 500 using Wikipedia
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    sp500_df = pd.read_html(url)[0]

    energy_tickers = sp500_df[sp500_df["GICS Sector"] == "Energy"]["Symbol"].tolist()

    print(energy_tickers)

    # Step 2: Use an API (e.g., yfinance or alternative) to fetch:
    #   - Historical trailing P/E ratio
    #   - Historical adjusted closing price
    #   - For the past 5 years (starting April 2020, ending April 2025)

    # Step 3: Loop through each month:
    #   - For each stock in the Energy sector:
    #       - Check the trailing P/E ratio at the beginning of the month
    #       - If P/E < 16.71:
    #           - If not currently holding it, BUY and record the price and entry date
    #           - If already holding, HOLD
    #       - If P/E >= 16.71 and currently holding:
    #           - SELL and record the sell price and exit date

    # Step 4: Repeat monthly until end of data

    # Step 5: Calculate returns:
    #   - Track each position's % return: (sell_price - buy_price) / buy_price
    #   - Log each trade
    #   - Compute:
    #       - Average return
    #       - Win rate
    #       - Max drawdown
    #       - Sharpe

    # Step 6: Save output to CSV and markdown logs

if __name__ == "__main__":
    main()