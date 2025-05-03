import requests
import json
import os
import pandas as pd
import numpy as np
from config import FMP_KEY, BASE_URL

def backtest(pe_path, sector_path, close_path, ticker, sector):
    # Load PE data for a ticker
    with open(pe_path) as f:
        pe_data = json.load(f)[ticker]

    # Load sector average PE for a sector
    with open(sector_path) as f:
        sector_avg_pe = json.load(f)[sector]

    # Load monthly close prices for a ticker
    with open(close_path) as f:
        close_data = json.load(f)[ticker]

    # Initalize portfolio value and monthly returns
    port_val = 100
    monthly_returns = {}
    dates = sorted(pe_data.keys())

    # For each month:
    for i in range(len(dates) - 1):
        month = dates[i]
        next_month = dates[i + 1]
        
        # Buy if undervalued
        if pe_data.get(month) is not None and sector_avg_pe.get(month) is not None:
            if pe_data[month] < sector_avg_pe[month]:
                # Calculate returns using closing prices
                try:
                    this_close = close_data[month]
                    next_close = close_data[next_month]
                    roi = (next_close / this_close) - 1
                    port_val *= (1 + roi)
                except KeyError:
                    continue

        monthly_returns[month] = round(port_val, 2)
    
    return monthly_returns


def calculate_metrics(portfolio_dict):
    values = list(portfolio_dict.values())
    dates = list(portfolio_dict.keys())
    start_val = values[0]
    end_val = values[-1]
    num_years = (pd.to_datetime(dates[-1]) - pd.to_datetime(dates[0])).days / 365.25

    # CAGR
    cagr = (end_val / start_val) ** (1 / num_years) - 1

    # Monthly returns
    returns = np.diff(values) / values[:-1]

    # Sharpe (assume risk-free rate = 0, monthly data)
    sharpe = (returns.mean() / returns.std()) * np.sqrt(12) if returns.std() != 0 else 0

    # Max drawdown
    peak = values[0]
    max_drawdown = 0
    for val in values:
        peak = max(peak, val)
        drawdown = (val - peak) / peak
        max_drawdown = min(max_drawdown, drawdown)
    
    print(f"CAGR: {cagr:.2%}")
    print(f"Sharpe Ratio: {sharpe:.2f}")
    print(f"Max Drawdown: {max_drawdown:.2%}")

def main():
    ticker = "XOM"
    sector = "energy"

    portfolio = backtest(
        "../data/pe.json",
        "../data/sector_average_pe.json",
        "../data/monthly_close.json",
        ticker,
        sector
    )

    calculate_metrics(portfolio)

if __name__ == "__main__":
    main()