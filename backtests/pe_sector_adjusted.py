import requests
from bs4 import BeautifulSoup   
import pandas as pd

def get_sector_tickers(sector):
    """Get tickers from a given GICS Sector from Wikipedia"""
    # Access Wikipedia's S&P 500 table and get tickers based on desired sector
    sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies" # Assign Wikipedia's S&P 500 url to a variable for easier manipulation or changing
    sp500_df = pd.read_html(sp500_url)[0] # Tell Pandas to read the html of the Wikipedias S&P 500 and grab the first table (which is the table for all stocks in the sp500)

    tickers = sp500_df[sp500_df["GICS Sector"] == f"{sector}"]["Symbol"].tolist() # Search the GICS Sector category for the desired sector, and when the specific sector is found, add that "Symbol"/ticker to the tickers list
    return tickers # Return the tickers list


def fetch_eps_data(ticker, shortName):
    """Get EPS data for a (temporarily hardcoded) url"""
    url = f"https://www.macrotrends.net/stocks/charts/XOM/exxon/eps-earnings-per-share-diluted"
    try: 
        # Access the website with XOM data and find the EPS table
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}) # Get a response from the URL and then include headers that make it seem more like a human and less likely to be flagged for spam
        response.raise_for_status() # If the response gave a status other than 200, raise an error
        soup = BeautifulSoup(response.text, "html.parser") # Tell BeautifulSoup to use their html parser on the html contents of the url
        tables = soup.find_all("table") # Use the parsed html to find all tables
        eps_table = tables[1] # Select the 2nd table which is the EPS table (found with trial and error)
        rows = eps_table.find_all("tr") # Find all rows in our EPS table

        # Loop through the rows and columns to fill the eps data dictionary 
        eps_data = {} # Have a blank dictionary that will be added to later 
        for row in rows[1:]: # Go through each row, skipping the header row which contains the titles ("date", "value")
            cols = row.find_all("td") # Find all table cells 
            if len(cols) >= 2: # Make sure that there is 2 cells of data to use in each row, one for the data, and one for the eps value
                date = cols[0].text.strip() # Grab the text date and remove whitespace
                eps_str = cols[1].text.strip().replace("$", "") # Grab the eps data as a string and remove whitespace and remove the $ sign
                eps = float(eps_str) # Convert the eps string to a float
                eps_data[date] = eps # Add each date and its corresponding eps to the eps data dict

        return eps_data

    except Exception as e: # If there are any exceptions in the above process then display that in a nice way
        print(f"Error fetching EPS for {ticker}: {e}")
        return {}

def main():
    # --- Step 1: Scrape list of Energy sector stocks from the S&P 500 using Wikipedia ---
    energy_tickers = get_sector_tickers("Energy")

    # --- Step 2: Scrape MacroTrends to find the following for each energy ticker: ---
    #   - EPS 
    #   - Historical adjusted closing price
    #   - For the past 5 years (starting April 2020, ending April 2025)
    xom_url = "https://www.macrotrends.net/stocks/charts/XOM/exxon/eps-earnings-per-share-diluted"
    eps_data = fetch_eps_data("XOM", xom_url)
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