import yfinance as yf
import json

def format_large_number(num):
    if not isinstance(num, (int, float)):
        return "N/A"
    
    units = [
        (1_000_000_000_000, "trillion"),
        (1_000_000_000, "billion"),
        (1_000_000, "million"),
    ]

    for threshold, label in units:
        if num >= threshold:
            return f"{num / threshold:.2f} {label}"
    
    return f"{num:,}"


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
    price = f"{price:.2f}" if isinstance(price, (int, float)) else "N/A"

    pe_ratio = info.get("trailingPE", "N/A")
    pe_ratio = f"{pe_ratio:.2f}" if isinstance(pe_ratio, (int, float)) else "N/A"

    dividend_yield = info.get("dividendYield", "N/A")
    dividend_yield = f"{dividend_yield * 100:.2f}%" if isinstance(dividend_yield, (int, float)) else "N/A"

    market_cap= format_large_number(info.get("marketCap"))
   
    fiftytwo_week_high_raw = info.get("fiftyTwoWeekHigh", "N/A")
    fiftytwo_week_high = f"{fiftytwo_week_high_raw:.2f}" if isinstance(fiftytwo_week_high_raw, (int, float)) else "N/A"

    fiftytwo_week_low_raw = info.get("fiftyTwoWeekLow", "N/A")
    fiftytwo_week_low = f"{fiftytwo_week_low_raw:.2f}" if isinstance(fiftytwo_week_low_raw, (int, float)) else "N/A"


    # Display extracted information
    print(f"Ticker: {ticker}")
    print(f"Company: {company}")
    print(f"Price: ${price}")
    print(f"P/E Ratio: {pe_ratio}")
    print(f"Dividend Yield: {dividend_yield}%")
    print(f"Market Cap: {market_cap}")
    print(f"52-Week High: {fiftytwo_week_high}")
    print(f"52-Week Low: {fiftytwo_week_low}")


    # Uncomment to see full JSON response from API
    # print(json.dumps(info, indent=2))


if __name__ == "__main__":
    main()