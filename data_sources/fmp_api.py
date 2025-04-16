from config import FMP_KEY
import requests

def main():
    ticker = "AAPL"
    url = f"https://financialmodelingprep.com/stable/search-symbol?query={ticker}&apikey={FMP_KEY}"
    response = requests.get(url)
    data = response.json()
    print(data)

if __name__ == "__main__":
    main()