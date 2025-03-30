# Stock Screener 📈

A Python app that fetches and displays basic stock data like price, P/E ratio, and dividend yield. Built using `yfinance`.

## Features

- ✅ Enter a stock ticker (e.g., `AAPL`)
- ✅ Fetch and display stock metrics:
  - Price
  - P/E ratio
  - Dividend yield
  - Market cap
  - 52-week high/low
- ✅ Recommend BUY, HOLD, or SELL based on basic rules

### Planned Features

- 🧠 Tune P/E-based strategy by testing it across different industries/sectors
- 📊 Add beta as a metric and include it in the recommendation logic

## Getting Started

### Requirements

- Python 3.9+
- `yfinance` package

### Setup

1. Clone this repo:

    ```bash
    git clone https://github.com/lucasfox0/stock_screener.git
    cd stock_screener
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the app:

    ```bash
    python app.py
    ```