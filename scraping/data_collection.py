import requests
import yfinance as yf
from bs4 import BeautifulSoup   
import pandas as pd
import re
import random
import time
from tqdm import tqdm
import json
from termcolor import colored
import datetime
import os

# --- Constants
WIKI_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
USER_AGENTS = [
    # Windows Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36", 
    # Mac Safari
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    # Firefox Linux
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0",
    # iPhone Safari
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    # Android Chrome
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.4896.127 Mobile Safari/537.36"
]
DELAY_RANGE = (60, 180)  # seconds
ACCEPT_LANGUAGES = [
    "en-US,en;q=0.9",
    "en-GB,en;q=0.8",
    "en;q=0.7",
    "fr-FR,fr;q=0.9,en;q=0.8",
]


def get_sector_tickers(sector):
    """Get tickers from a given GICS Sector from Wikipedia"""
    # Access Wikipedia's S&P 500 table and get tickers based on desired sector
    sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies" # Assign Wikipedia's S&P 500 url to a variable for easier manipulation or changing
    sp500_df = pd.read_html(sp500_url)[0] # Tell Pandas to read the html of the Wikipedias S&P 500 and grab the first table (which is the table for all stocks in the sp500)

    tickers = sp500_df[sp500_df["GICS Sector"] == f"{sector}"]["Symbol"].tolist() # Search the GICS Sector category for the desired sector, and when the specific sector is found, add that "Symbol"/ticker to the tickers list
    return tickers # Return the tickers list


def build_macrotrends_url(ticker):
    """Build the url used for scraping MacroTrends"""
    short_name = yf.Ticker(ticker).info.get("shortName")

    # Ensure that the short name actually exists
    if not short_name:
        print(f"Could not find shortName for {ticker}")
        return None

    slug = re.sub(r'[^a-z0-9]+', '-', short_name.lower()).strip('-') # Replace any unconventional characters with dashes

    return f"https://www.macrotrends.net/stocks/charts/{ticker}/{slug}/eps-earnings-per-share-diluted"


def fetch_eps_data(ticker, url):
    """Get EPS data for a (temporarily hardcoded) url"""
    try: 
        # Access the website with ticker data and find the EPS table
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept-Language": random.choice(ACCEPT_LANGUAGES)
        }
        print(f"Using {headers}") # for debugging
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, "html.parser")
        tables = soup.find_all("table")
        eps_table = tables[1] # EPS table
        rows = eps_table.find_all("tr") 

        # Loop through the rows and columns to fill the eps data dictionary 
        eps_data = {} 
        for row in rows[1:]:
            cols = row.find_all("td") 
            if len(cols) >= 2:
                date = cols[0].text.strip() 
                eps_str = cols[1].text.strip().replace("$", "") 
                eps = float(eps_str) 
                eps_data[date] = eps 

        return eps_data

    except Exception as e:
        print(f"Error fetching EPS for {ticker}: {e}")
        return {}
    

def scrape_ticker_eps(ticker, max_attempts=3):
    """Attempt to scrape EPS data for a given ticker up to max_attempts"""
    attempts = 0
    while attempts < max_attempts:
        url = build_macrotrends_url(ticker)
        if not url:
            print(colored(f"No URL built for {ticker}", "red"))
            return None, f"No URL built for {ticker}"
        
        eps_data = fetch_eps_data(ticker, url)
        if eps_data:
            return {
                "eps": eps_data,
                "meta": {
                    "scraped_at": datetime.datetime.now().isoformat(),
                    "source": "MacroTrends"
                }
            }, None
        
        attempts += 1

        # Apply a delay that increases with each attempt
        print(colored(f"{attempts} try for {ticker}...", "yellow"))
        time.sleep(random.uniform(*DELAY_RANGE) + attempts * 30)
        
    return None, f"Failed to fetch EPS for {ticker} after {max_attempts} attempts"


    

def collect_and_save_eps_data(output_path):
    """Main scraper: loops through all tickers in a sector and saves EPS data to a JSON file """
    # Scrape list of Energy sector stocks from the S&P 500 using Wikipedia 
    energy_tickers = get_sector_tickers("Energy")

    # Scrape MacroTrends to find the EPS for each energy ticker 
    all_eps_data = {}
    failed_tickers_log = {}

    for ticker in tqdm(energy_tickers, desc="Scraping EPS"):
        print(f"\nStarting {ticker}...")
        data, error = scrape_ticker_eps(ticker)

        if data:
            all_eps_data[ticker] = data
            delay = random.uniform(*DELAY_RANGE)
            print(colored(f"Finished {ticker} - sleeping {delay:.0f} seconds", "green"))
            time.sleep(delay)
        else:
            print(colored(f"Error with {ticker}: {error}", "red"))
            failed_tickers_log[ticker] = error

    # Convert EPS dict to a JSON file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(all_eps_data, f, indent=2)

    print(f"\nEPS data saved to {output_path}")

    # If any tickers failed, display that here
    if failed_tickers_log:
        print(colored("The following tickers failed:", "red"))
        for t, err in failed_tickers_log.items():
            print(f"{t}: {err}")


def main():
    print(colored("Starting code...", "blue"))
    collect_and_save_eps_data(output_path="../data/eps_energy.json")
    print("✅ Code complete")

if __name__ == "__main__":
    main()