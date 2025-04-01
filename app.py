import yfinance as yf
import json

# --- Helper function to format large numbers ---
def format_large_number(num):
    """
    Args:
        num (int or float): The number to format  
    Returns:
        str: Human-readable string using "million", "billion", or "trillion" for large numbers,
                or with commas for smaller values
    """

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


# --- Function to get a stock ticker input ---
def get_valid_ticker():
    """
    Returns:
        str: Validated and uppercased stock ticker
    """
    while True: 
        ticker = input("Enter a stock ticker: ").strip().upper()
    
        if not ticker.isalpha() or len(ticker) < 1:
            print("Invalid ticker. Please enter a valid stock symbol.\n") 
        else: 
            return ticker


# --- Function to fetch stock data using yfinance ---
def get_stock_info(ticker):
    """
    Args:
        ticker (str): Stock ticker symbol
    Returns:
        dict: Stock info dictionary from yfinance
    """
    return yf.Ticker(ticker).info


# --- Function to extract key metrics used in strategies ---
def extract_metrics(info):
    """
    Args:
        info (dict): yfinance stock info
    Returns:
        dict: Cleaned and formatted metrics
    """
    # Get raw data for metrics that need to be formatted
    price_val = info.get("currentPrice", "N/A")
    pe_ratio_val = info.get("trailingPE", "N/A")
    div_yield_val = info.get("dividendYield", "N/A")
    high_52w_val = info.get("fiftyTwoWeekHigh", "N/A")
    low_52w_val = info.get("fiftyTwoWeekLow", "N/A")

    return {
        "company": info.get("shortName", "N/A"),
        "sector": info.get("sector", "N/A"),
        "price": f"{price_val:.2f}" if isinstance(price_val, (int, float)) else "N/A",
        "pe_ratio_val": pe_ratio_val,
        "pe_ratio": f"{pe_ratio_val:.2f}" if isinstance(pe_ratio_val, (int, float)) else "N/A",
        "dividend_yield_val": info.get("dividendYield", "N/A"),
        "dividend_yield": f"{div_yield_val * 100:.2f}%" if isinstance(div_yield_val, (int, float)) else "N/A",
        "beta": info.get("beta", "N/A"),
        "market_cap": format_large_number(info.get("marketCap")),
        "high_52w": f"{high_52w_val:.2f}" if isinstance(high_52w_val, (int, float)) else "N/A",
        "low_52w": f"{low_52w_val:.2f}" if isinstance(low_52w_val, (int, float)) else "N/A"
    }


# --- Function to print extracted key metrics ---
def print_metrics(ticker, metrics):
    """
    Args:
        ticker (str): Stock ticker
        metrics (dict): Dictionary of stock metrics
    """
    print(f"\nTicker:         {ticker}")
    print(f"Company:        {metrics['company']}")
    print(f"Sector:         {metrics['sector']}")
    print(f"Price:          ${metrics['price']}")
    print(f"P/E Ratio:      {metrics['pe_ratio']}")
    print(f"Dividend Yield: {metrics['dividend_yield']}")
    print(f"Beta:           {metrics['beta']}")
    print(f"Market Cap:     {metrics['market_cap']}")
    print(f"52-Week High:   ${metrics['high_52w']}")
    print(f"52-Week Low:    ${metrics['low_52w']}")


# --- Function to execute appropriate strategy and get recommendation to BUY/HOLD/SELL ---
def get_recommendation(metrics):
    """
    Args:
        metrics (dict): Dictionary of stock metrics
    Returns:
        str: Recommendation string
    """
    sector = metrics["sector"]
    pe_ratio_val = metrics["pe_ratio_val"]
    beta = metrics["beta"]

    # Average P/E's for mean-reverting sectors
    sector_pe_averages = {
        "Consumer Defensive": 23.23,
        "Utilities": 20.71,
        "Financial Services": 18.01,
        "Energy": 16.71
    }

    # Use P/E-based recommendation for mean-reverting sectors, otherwise use beta-based logic
    if sector in sector_pe_averages:
        avg_pe = sector_pe_averages.get(sector, 20)
        if isinstance(pe_ratio_val, (int, float)):
            print(f"(Based on sector-average P/E of {avg_pe} for {sector})")
            if pe_ratio_val < avg_pe:
                return "BUY"
            elif pe_ratio_val > 30:
                return "SELL"
            else:
                return "HOLD"
        else:
            return "Insufficient P/E data for recommendation."
    else:
        if isinstance(beta, (int, float)):
            print(f"(Based on beta strategy for non-mean-reverting {sector} sector)")
            if beta < 0.9:
                return "BUY"
            elif beta > 1.2:
                return "SELL"
            else:
                return "HOLD"
        else:
            return "Insufficient beta data for recommendation."


def main():
    ticker = get_valid_ticker()
    info = get_stock_info(ticker)
    metrics = extract_metrics(info)

    print_metrics(ticker, metrics)

    print(f"\n --- RECOMMENDATION ---")
    print(get_recommendation(metrics))

    print("\n\n")

    # --- Uncomment to see full JSON response from yfinance (for debugging) ---
    # print(json.dumps(info, indent=2))


if __name__ == "__main__":
    main()