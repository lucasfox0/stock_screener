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
        "from": "2014-12-15",
        "to": "2024-12-15",
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

    return f"Montly close data saved to {output_path}", None

def get_quarterly_eps(ticker, output_path):
    """Get the quarterly EPS of a ticker"""
    endpoint = f"{BASE_URL}/v3/income-statement-as-reported/{ticker}"
    params = {
        "period": "quarter",
        "limit": 40,
        "apikey": FMP_KEY
    }

    # Make a GET request to fetch data and parse the JSON
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return None, f"Error fetching data: {e}"
    
    eps_data = {}
    for quarter in data:
        date = quarter.get("date")
        eps = quarter.get("earningspersharediluted")

        if data and eps is not None:
            eps_data[date] = round(eps, 2)
        
    # Nest EPS data inside another dict with tickers
    eps_dict = {
        ticker: eps_data
    }

    # Save eps dict to JSON
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(eps_dict, f, indent=2)

    return f"Saved EPS dict to {output_path}", None


def main():
    monthly_close_data, monthly_close_error = get_monthly_closing_price("XOM", "../data/monthly_close.json")
    if monthly_close_data:
        print(monthly_close_data)
    else:
        print(monthly_close_error)

    # quarterly_eps_data, quarterly_eps_error = get_quarterly_eps("XOM", "../data/quarterly_eps.json")
    # if quarterly_eps_data:
    #     print(json.dumps(quarterly_eps_data, indent=2))
    # else:
    #     print(quarterly_eps_error)

if __name__ == "__main__":
    main()