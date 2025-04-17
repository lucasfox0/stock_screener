import requests
import json
import os
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

# Old method for fetching historical P/E. Now used since P/E is being calculated manually
def deprecated_get_historical_pe(tickers, output_path):
    """Save historical P/E data for a list of tickers to a JSON"""
    params = {
        "period": "quarter",
        "limit": 40,
        "apikey": FMP_KEY
    }

    historical_pe = {} # Main dictionary to store all P/E data
    for ticker in tickers:
        # Build endpoint URL using the ticker and set limit=40 (10 years of quarterly data)
        endpoint = f"{BASE_URL}/v3/ratios/{ticker}"
        
        # Make GET request to fetch data and parse the JSON response
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            return None, f"Error fetching data: {e}"

        # Extract the "priceEarningsRatio" from each quarterly entry
        for quarter in data:
            date = quarter["date"]
            pe = quarter["priceEarningsRatio"]

            if ticker not in historical_pe:
                historical_pe[ticker] = {}
            
            historical_pe[ticker][date] = pe

    # Save the historical_pe dict to a JSON
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(historical_pe, f, indent=2)

    print(f"\nP/E data saved to {output_path}")


def main():
    energy_tickers, error = get_tickers("Energy")

if __name__ == "__main__":
    main()