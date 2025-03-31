import yfinance as yf
import json

# --- Helper function to format large numbers ---
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
            print("Invalid ticker. Please enter a valid stock symbol.\n") 
        else: 
            break

    # Fetch stock data using yfiance
    dat = yf.Ticker(ticker)
    info = dat.info

    # --- Extract key metrics from the stock info ---
    company = info.get("shortName", "N/A")

    sector = info.get("sector")

    price = info.get("currentPrice", "N/A")
    price = f"{price:.2f}" if isinstance(price, (int, float)) else "N/A"

    pe_ratio_val = info.get("trailingPE", "N/A")
    pe_ratio = f"{pe_ratio_val:.2f}" if isinstance(pe_ratio_val, (int, float)) else "N/A"

    dividend_yield_val = info.get("dividendYield", "N/A")
    dividend_yield = f"{dividend_yield_val * 100:.2f}%" if isinstance(dividend_yield_val, (int, float)) else "N/A"

    market_cap = format_large_number(info.get("marketCap"))
   
    high_52w = info.get("fiftyTwoWeekHigh", "N/A")
    high_52w = f"{high_52w:.2f}" if isinstance(high_52w, (int, float)) else "N/A"

    low_52w = info.get("fiftyTwoWeekLow", "N/A")
    low_52w = f"{low_52w:.2f}" if isinstance(low_52w, (int, float)) else "N/A"

    # Hard coded industry average P/E (for MVP only)
    industry_avg_pe = 20

    # --- Display extracted information ---
    print(f"Ticker: {ticker}")
    print(f"Company: {company}")
    print(f"Sector: {sector}")
    print(f"Price: ${price}")
    print(f"P/E Ratio: {pe_ratio}")
    print(f"Dividend Yield: {dividend_yield}")
    print(f"Market Cap: {market_cap}")
    print(f"52-Week High: {high_52w}")
    print(f"52-Week Low: {low_52w}")

    # --- Display recommendation based on P/E ratio and dividend yield ---
    print(f"\n --- RECOMMENDATION ---")
    if isinstance(pe_ratio_val, (int, float)) and isinstance(dividend_yield_val, (int, float)):
        if pe_ratio_val < industry_avg_pe and dividend_yield_val > 0.01:
            print("BUY")
        elif pe_ratio_val > 30:
            print("SELL")
        else:
            print("HOLD")
    else:
        print("Insufficent data to make recommendation.")


    # --- Uncomment to see full JSON response from API ---
    # print(json.dumps(info, indent=2))


if __name__ == "__main__":
    main()