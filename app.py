import yfinance as yf
import json

def main():

    # Prompt user for a stock sticker; ensure it's alphabetical and not empty
    while True: 
        ticker = input ("Enter a stock ticker: ").strip().upper()
    
        if not ticker.isalpha() or len(ticker) < 1:
            print("Invalid ticker. Please enter a valid stock symbol \n") 
        else: 
            break

    # Fetch stock data using yfiance
    dat = yf.Ticker(ticker)
    info = dat.info

    # Extract key metrics from the stock info
    company = info.get("shortName", "N/A")
    price = info.get("currentPrice", "N/A")
    pe_ratio = info.get("trailingPE", "N/A")
    dividend_yield = info.get("dividendYield", "N/A")
    market_cap = info.get("marketCap", "N/A")
    fiftytwo_week_high = info.get("fiftyTwoWeekHigh", "N/A")
    fiftytwo_week_low = info.get("fiftyTwoWeekLow", "N/A")

    # Display extracted information
    print(f"Ticker: {ticker}")
    print(f"Company: {company}")
    print(f"Price: ${price}")
    print(f"P/E Ratio: {pe_ratio}")
    print(f"Dividend Yield: {dividend_yield}")
    print(f"Market Cap: {market_cap}")
    print(f"52-Week High: {fiftytwo_week_high}")
    print(f"52-Week Low: {fiftytwo_week_low}")

    # Uncomment to see full JSON response from API
    # print(json.dumps(info, indent=2))


if __name__ == "__main__":
    main()