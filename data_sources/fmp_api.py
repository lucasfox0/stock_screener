import requests
import json
import os
import pandas as pd
import numpy as np
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

    for date in close_series.index: # Lopp through each row(or date) in the monthly closing price index
        valid_eps_dates = eps_series.index[eps_series.index <= date] # I believe this is getting a list of all the valid eps rows that are either less than or equal to the date. for example if the date is 2016-07-1, this would return something like 2015 12-01, 2015, 9-01... 2014... etc
        if not valid_eps_dates.empty: # If THERE ARE a list or dates that are less than or equal to the date
            latest_eps_date = valid_eps_dates[-1] # Use the last eps data in that list (closest to our date)
            eps = eps_series[latest_eps_date] # save the eps value

            if eps != 0: 
                pe_ratio = close_series[date] / eps # Divide the the close by the eps to get PE
                pe_data[date.strftime("%Y-%m-%d")] = round(pe_ratio, 2) # Add to the pe data dict under the date, converted to a string, and the pe ratio as a value rounded to 2 decimals

    pe_dict = {
        ticker: pe_data
    }
    
    # Convert the P/E dictionary into JSON and save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(pe_dict, f, indent=2)

    return f"Saved P/E data to {output_path}", None


def backtest(pe_path, sector_path, close_path, ticker, sector):
    # Load PE data for all tickers
    with open(pe_path) as f:
        pe_data = json.load(f)[ticker]

    # Load sector average PE
    with open(sector_path) as f:
        sector_avg_pe = json.load(f)[sector]

    # Load monthly close prices
    with open(close_path) as f:
        close_data = json.load(f)[ticker]

    # Initalize portfolio value and monthly returns
    port_val = 100
    monthly_returns = {}
    dates = sorted(pe_data.keys())

    # For each month:
    for i in range(len(dates) - 1):
        month = dates[i]
        next_month = dates[i + 1]
        
        # Buy if undervalued
        if pe_data.get(month) is not None and sector_avg_pe.get(month) is not None:
            if pe_data[month] < sector_avg_pe[month]:
                # Calculate returns using closing prices
                try:
                    this_close = close_data[month]
                    next_close = close_data[next_month]
                    roi = (next_close / this_close) - 1
                    port_val *= (1 + roi)
                except KeyError:
                    continue

        monthly_returns[month] = round(port_val, 2)

    # Save portfolio value for this month
    with open("../data/portfolio_value.json", "w") as f:
        json.dump(monthly_returns, f, indent=2)
    
    return monthly_returns


def calculate_metrics(portfolio_dict):
    values = list(portfolio_dict.values())
    dates = list(portfolio_dict.keys())
    start_val = values[0]
    end_val = values[-1]
    num_years = (pd.to_datetime(dates[-1]) - pd.to_datetime(dates[0])).days / 365.25

    # CAGR
    cagr = (end_val / start_val) ** (1 / num_years) - 1

    # Monthly returns
    returns = np.diff(values) / values[:-1]

    # Sharpe (assume risk-free rate = 0, monthly data)
    sharpe = (returns.mean() / returns.std()) * np.sqrt(12) if returns.std() != 0 else 0

    # Max drawdown
    peak = values[0]
    max_drawdown = 0
    for val in values:
        peak = max(peak, val)
        drawdown = (val - peak) / peak
        max_drawdown = min(max_drawdown, drawdown)
    
    print(f"CAGR: {cagr:.2%}")
    print(f"Sharpe Ratio: {sharpe:.2f}")
    print(f"Max Drawdown: {max_drawdown:.2%}")

def main():
    ticker = "XOM"
    sector = "energy"

    portfolio = backtest(
        "../data/pe.json",
        "../data/sector_average_pe.json",
        "../data/monthly_close.json",
        ticker,
        sector
    )

    calculate_metrics(portfolio)

if __name__ == "__main__":
    main()