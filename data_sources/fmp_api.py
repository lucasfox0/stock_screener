import requests
import json
import os
import pandas as pd
from config import FMP_KEY, BASE_URL


def get_tickers(sector):
    """Return a list of energy tickers"""
    endpoint = f"{BASE_URL}/v3/stock-screener"
    params = {
        "isActivelyTrading": True,
        "exchange": "nyse",
        "marketCapMoreThan": 10_000_000_000, # 10B (Large Cap)
        "isEtf": "false",
        "isFund": "false",
        "sector": sector,
        "apikey": FMP_KEY
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return None, f"Error fetching data: {e}"
    
    # Extract ticker symbols from each dictionary in the response
    tickers = [item["symbol"] for item in data]

    return tickers, None


def get_monthly_closing_price(ticker, output_path):
    """Get the monthly closing price of a ticker"""
    endpoint = f"{BASE_URL}/v3/historical-price-full/{ticker}"
    params = {
        "from": "2014-01-01",
        "to": "2024-01-01",
        "apikey": FMP_KEY
    }

    # Make GET request to fetch data and parse the JSON response
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return None, f"Error fetching data: {e}"
    
    df = pd.DataFrame(data["historical"]) # Convert list of dict into a pandas DataFrame
    df["date"] = pd.to_datetime(df["date"]) # Convert dates (strings) into datetime objects
    df.set_index("date", inplace=True) # Set the table index to the dates
    df.sort_index(inplace=True)
    monthly_close = df["close"].resample("ME").last() # Group all rows by month and return the last value of each month

    monthly_close.index = monthly_close.index.strftime("%Y-%m-%d") # Convert the date index into strings

    # Convert the pandas Series into a nested dictionary where the date is the key and monthly close is the value
    monthly_close_dict = {
        ticker: monthly_close.round(2).to_dict()
    }

    # Convert monthly close dict to a JSON file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(monthly_close_dict, f, indent=2)

    print(f"Montly close data saved to {output_path}")


def main():
    monthly_close = get_monthly_closing_price("XOM", "../data/monthly_close.json")

if __name__ == "__main__":
    main()