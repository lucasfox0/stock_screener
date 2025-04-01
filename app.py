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
    # Prompt user for a stock ticker; ensure it's alphabetical and not empty
    while True: 
        ticker = input("Enter a stock ticker: ").strip().upper()
    
        if not ticker.isalpha() or len(ticker) < 1:
            print("Invalid ticker. Please enter a valid stock symbol.\n") 
        else: 
            break

    # Fetch stock data using yfinance
    dat = yf.Ticker(ticker)
    info = dat.info

    # --- Extract key metrics from the stock info ---
    company = info.get("shortName", "N/A")

    sector = info.get("sector", "N/A")

    price = info.get("currentPrice", "N/A")
    price = f"{price:.2f}" if isinstance(price, (int, float)) else "N/A"

    pe_ratio_val = info.get("trailingPE", "N/A")
    pe_ratio = f"{pe_ratio_val:.2f}" if isinstance(pe_ratio_val, (int, float)) else "N/A"

    dividend_yield_val = info.get("dividendYield", "N/A")
    dividend_yield = f"{dividend_yield_val * 100:.2f}%" if isinstance(dividend_yield_val, (int, float)) else "N/A"

    beta = info.get("beta", "N/A")

    market_cap = format_large_number(info.get("marketCap"))
   
    high_52w = info.get("fiftyTwoWeekHigh", "N/A")
    high_52w = f"{high_52w:.2f}" if isinstance(high_52w, (int, float)) else "N/A"

    low_52w = info.get("fiftyTwoWeekLow", "N/A")
    low_52w = f"{low_52w:.2f}" if isinstance(low_52w, (int, float)) else "N/A"

    # --- Display extracted information ---
    print(f"\nTicker:         {ticker}")
    print(f"Company:        {company}")
    print(f"Sector:         {sector}")
    print(f"Price:          ${price}")
    print(f"P/E Ratio:      {pe_ratio}")
    print(f"Dividend Yield: {dividend_yield}")
    print(f"Beta:           {beta}")
    print(f"Market Cap:     {market_cap}")
    print(f"52-Week High:   {high_52w}")
    print(f"52-Week Low:    {low_52w}")

    # --- Display recommendation based on sector-aware logic ---
    sector_pe_averages = {
        "Consumer Defensive": 23.23,
        "Utilities": 20.71,
        "Financial Services": 18.01,
        "Energy": 16.71
    }

    # Use P/E-based recommendation for mean-reverting sectors, otherwise use beta-based logic
    print(f"\n --- RECOMMENDATION ---")

    if sector in sector_pe_averages.keys():
        avg_pe = sector_pe_averages.get(sector, 20)
        if isinstance(pe_ratio_val, (int, float)):
            print(f"(Based on sector-average P/E for {sector})")
            if pe_ratio_val < avg_pe:
                print("BUY")
            elif pe_ratio_val > 30:
                print("SELL")
            else:
                print("HOLD")
        else:
            print("Insufficient P/E data for recommendation.")
    else:
        if isinstance(beta, (int, float)):
            print(f"(Based on beta strategy for non-mean-reverting sector {sector})")
            if beta < 0.9:
                print("BUY")
            elif beta > 1.2:
                print("SELL")
            else:
                print("HOLD")
        else:
            print("Insufficient beta data for recommendation.")


    print("\n\n")

    # --- Uncomment to see full JSON response from API ---
    # print(json.dumps(info, indent=2))


if __name__ == "__main__":
    main()