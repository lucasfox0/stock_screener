# Stock Screener 📈

A Python-based terminal app that fetches and analyzes key stock metrics like price, P/E ratio, dividend yield, and market cap. It also provides a basic BUY, HOLD, or SELL recommendation based on customizable logic.

> 📦 **Status: Alpha**  
> MVP complete. Now adding smarter screening logic, tuning by sector, and laying the groundwork for future quant features.

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