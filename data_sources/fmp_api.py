import requests
import json
from config import FMP_KEY, BASE_URL

def get_energy_tickers():
    """Return a list of energy tickers"""
    endpoint = f"{BASE_URL}/v3/stock-screener"
    params = {
        "isActivelyTrading": True,
        "exchange": "nyse",
        "marketCapMoreThan": 10_000_000_000, # 10B (Large Cap)
        "isEtf": "false",
        "isFund": "false",
        "sector": "Energy",
        "apikey": FMP_KEY
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return None, f"Error fetching data: {e}"
    
    # Extract ticker symbols from each dictionary in the response
    energy_tickers = [item["symbol"] for item in data]

    return energy_tickers, None


def main():
    energy_tickers, error = get_energy_tickers()

if __name__ == "__main__":
    main()