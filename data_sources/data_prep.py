import requests
import json
import os
import pandas as pd
import numpy as np
from config import FMP_KEY, BASE_URL


# CHECK FOR UNUSED LIBS ^^^

def get_tickers(sector, output_path):
    """Return a list of large cap ticker symbols for a specified sector"""
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

    # Save to JSON
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(tickers, f, indent=2)

    return f"Large cap {sector} tickers saved to {output_path}", None


def get_monthly_closing_price(ticker, output_path):
    """Get the monthly closing price of a ticker"""
    endpoint = f"{BASE_URL}/v3/historical-price-full/{ticker}"
    params = {
        "from": "2014-12-15",
        "to": "2024-12-15",
        "apikey": FMP_KEY
    }

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

    eps_dict = {
        ticker: eps_data
    }

    # Save eps dict to JSON
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(eps_dict, f, indent=2)

    return f"Saved EPS dict to {output_path}", None


def calculate_monthly_pe(ticker, output_path):
    """Calculate the monthly P/E given monthly close price and quarterly EPS"""
    # Load close data and eps data
    with open("../data/monthly_close.json") as f:
        close_data = json.load(f)[ticker]
    with open("../data/quarterly_eps.json") as f:
        eps_data = json.load(f)[ticker]

    # Convert close data and eps data to pandas.Series, where the date is datetime and sorted chronologically
    close_series = pd.Series(close_data)
    close_series.index = pd.to_datetime(close_series.index)
    close_series = close_series.sort_index()

    eps_series = pd.Series(eps_data)
    eps_series.index = pd.to_datetime(eps_series.index)
    eps_series = eps_series.sort_index()

    # Initalize an empty dict to store P/E values
    pe_data = {}
    for date in close_series.index:
        valid_eps_dates = eps_series.index[eps_series.index <= date]
        if not valid_eps_dates.empty:
            latest_eps_date = valid_eps_dates[-1] 
            eps = eps_series[latest_eps_date]

            if eps != 0: 
                pe_ratio = close_series[date] / eps 
                pe_data[date.strftime("%Y-%m-%d")] = round(pe_ratio, 2) 

    pe_dict = {
        ticker: pe_data
    }
    
    # Convert the P/E dictionary into JSON and save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(pe_dict, f, indent=2)

    return f"Saved P/E data to {output_path}", None


def main():
    sector = "Energy"
    
    data, err = get_tickers(sector, f"../data/large_cap_{sector}_tickers.json")
    if data:
        print(data)
    else:
        print(err)

if __name__ == "__main__":
    main()