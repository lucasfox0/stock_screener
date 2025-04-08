import requests
from bs4 import BeautifulSoup   
import pandas as pd

def main():
    # Step 1: Scrape list of Energy sector stocks from the S&P 500 using Wikipedia
    energy_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    sp500_df = pd.read_html(energy_url)[0]

    energy_tickers = sp500_df[sp500_df["GICS Sector"] == "Energy"]["Symbol"].tolist()

    print(energy_tickers)

    # Step 2: Use an API (e.g., yfinance or alternative) to fetch:
    #   - Historical trailing P/E ratio
    #   - Historical adjusted closing price
    #   - For the past 5 years (starting April 2020, ending April 2025)
    
    # Use BeautifulSoup to get the table with EPS data
    xom_url = "https://www.macrotrends.net/stocks/charts/XOM/exxon/eps-earnings-per-share-diluted"
    response = requests.get(xom_url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")

    tables = soup.find_all("table")
    eps_table = tables[1]
    rows = eps_table.find_all("tr")

    eps_data = {}

    for row in rows[1:]: # Skip header row
        cols = row.find_all("td")
        if len(cols) >= 2:
            date = cols[0].text.strip()
            eps_str = cols[1].text.strip().replace("$", "")
            eps = float(eps_str)

            eps_data[date] = eps

    print(eps_data)



    # Step 3: Loop through each month (starting at the first trading day of each month):
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