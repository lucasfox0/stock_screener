# Stock Screener 📈

A Python-based terminal app that fetches and displays stock data using `yfinance`. It provides a sector-aware BUY/HOLD/SELL recommendation based on either P/E ratio or beta, depending on which strategy is more appropriate for the sector.


## Demo

![Stock Screener Demo](demo.png)

## Features

- Enter a stock ticker (e.g., `AAPL`)
- Fetch and display stock metrics:
  - Company name
  - Sector
  - Price
  - P/E ratio
  - Dividend yield
  - Beta
  - Market cap
  - 52-week high/low
- Recommend BUY, HOLD, or SELL based on:
  - **P/E ratio** (for mean-reverting sectors)
  - **Beta** (for all other sectors)

## Strategy Summary

| Sector Type           | Strategy Used    | Logic                                                           |
|-----------------------|------------------|-----------------------------------------------------------------|
| Mean-Reverting Sectors| P/E Ratio        | BUY if P/E < sector average, SELL if P/E > 30, else HOLD        |
| Other Sectors         | Beta             | BUY if beta < 0.9, SELL if beta > 1.2, else HOLD                |

📌 *Mean-reverting sectors include: Consumer Defensive, Utilities, Financial Services, and Energy*

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