import yfinance as yf
import json

def main():
    while True:
        ticker = input ("Enter a stock ticker: ").strip().upper()
    
        if not ticker.isalpha() or len(ticker) < 1:
            print("Invalid ticker. Please enter a valid stock symbol \n") 
        else: 
            break

    dat = yf.Ticker(ticker)
    info = dat.info

    print(json.dumps(info, indent=2))

if __name__ == "__main__":
    main()