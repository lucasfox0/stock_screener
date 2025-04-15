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
from config import WIKI_URL, USER_AGENTS, DELAY_RANGE, ACCEPT_LANGUAGES, SMARTPROXY_USERNAME, SMARTPROXY_PASSWORD, MAX_ATTEMPTS


def get_sector_tickers(sector):
    """Get tickers from a given GICS Sector from Wikipedia"""
    sp500_df = pd.read_html(WIKI_URL)[0]

    tickers = sp500_df[sp500_df["GICS Sector"] == f"{sector}"]["Symbol"].tolist()
    return tickers


def build_macrotrends_url(ticker):
    """Build the url used for scraping MacroTrends"""
    # Get short name from yFinance
    info = yf.Ticker(ticker).info
    try:
        short_name = info.get("shortName")
    except Exception:
        short_name = None

    if not short_name:
        return None

    slug = re.sub(r'[^a-z0-9]+', '-', short_name.lower()).strip('-') # Replace any unconventional characters with dashes

    return f"https://www.macrotrends.net/stocks/charts/{ticker}/{slug}/eps-earnings-per-share-diluted"


def fetch_eps_data(ticker, url):
    """Get EPS data for a url"""
    try:
        # Access the website with ticker data and find the EPS table
        headers = { # Human-like headers
            "User-Agent": random.choice(USER_AGENTS),
            "Accept-Language": random.choice(ACCEPT_LANGUAGES),
        }
        proxy = {
            "http": f"http://{SMARTPROXY_USERNAME}:{SMARTPROXY_PASSWORD}@gate.smartproxy.com:10001",
            "https": f"http://{SMARTPROXY_USERNAME}:{SMARTPROXY_PASSWORD}@gate.smartproxy.com:10001"
        }
        response = requests.get(url, headers=headers, proxies=proxy, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        tables = soup.find_all("table")

        if len(tables) < 2:
            raise ValueError("Expected EPS table not found. Likely CAPTCHA.")

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
    

def scrape_ticker_eps(ticker, max_attempts=MAX_ATTEMPTS):
    """Attempt to scrape EPS data for a given ticker up to MAX_ATTEMPTS"""
    attempts = 0
    while attempts < max_attempts:
        url = build_macrotrends_url(ticker)
        if not url:
            return None, f"No URL built for {ticker}"
        
        eps_data = fetch_eps_data(ticker, url)
        if eps_data:
            return {
                "eps": eps_data,
                "meta": {
                    "scraped_at": datetime.datetime.now().isoformat(),
                    "source": "MacroTrends",
                    "attempts": attempts
                }
            }, None
        

        # Apply a delay that increases exponentially with each attempt
        delay = min(random.uniform(*DELAY_RANGE) * (1.7 ** attempts), 300)
        print(colored(f"{attempts + 1} try for {ticker} - sleeping {delay:.0f} seconds...", "yellow"))

        attempts += 1

        time.sleep(delay)
        
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

    if not SMARTPROXY_USERNAME or not SMARTPROXY_PASSWORD:
        raise Exception("Missing Smartproxy credentials")
    else:
        collect_and_save_eps_data(output_path="../data/eps_energy.json")
    print("✅ Code complete")

if __name__ == "__main__":
    main()