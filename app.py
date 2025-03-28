import yfinance as yf
import json

def main():
    dat = yf.Ticker("AAPL")
    info = dat.info

    print(json.dumps(info, indent=2))

if __name__ == "__main__":
    main()