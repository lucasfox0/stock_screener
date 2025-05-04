import json
import os
import pandas as pd
import numpy as np

def backtest(pe_all, sector_avg_pe, close_all):
    # Initalize portfolio value and monthly returns
    port_val = 100 
    monthly_returns = {}

    # Get the full date range across all tickers
    all_dates = set()
    for pe_data in pe_all.values():
        all_dates.update(pe_data.keys())
    dates = sorted(all_dates) # convert set to a sorted list

    # Loop over each month except the last, so we can safely access month and next_month pairs
    for i in range(len(dates) - 1):
        month = dates[i]
        next_month = dates[i + 1]

        # Build list of tickers to trade this month: must have PE and close data, be undervalued vs sector, and have next month's close price
        active_tickers = []
        for ticker in pe_all:
            pe_data = pe_all[ticker]
            close_data = close_all.get(ticker)

            if not close_data:
                continue

            if pe_data.get(month) is not None and sector_avg_pe.get(month) is not None:
                if pe_data[month] < sector_avg_pe[month]:
                    if month in close_data and next_month in close_data:
                        active_tickers.append(ticker)

        if active_tickers:
            roi_sum = 0
            for ticker in active_tickers:
                this_close = close_all[ticker][month]
                next_close = close_all[ticker][next_month]
                roi = (next_close / this_close) - 1
                roi_sum += roi
            
            avg_roi = roi_sum / len(active_tickers)
            port_val *= (1 + avg_roi)

        monthly_returns[month] = round(port_val, 2)
    
    return monthly_returns


def calculate_metrics(portfolio_dict):
    values = list(portfolio_dict.values())
    dates = list(portfolio_dict.keys())
    start_val = values[0]
    end_val = values[-1]
    num_years = (pd.to_datetime(dates[-1]) - pd.to_datetime(dates[0])).days / 365.25

    cagr = (end_val / start_val) ** (1 / num_years) - 1
    returns = np.diff(values) / values[:-1]
    sharpe = (returns.mean() / returns.std()) * np.sqrt(12) if returns.std() != 0 else 0

    peak = values[0]
    max_drawdown = 0
    for val in values:
        peak = max(peak, val)
        drawdown = (val - peak) / peak
        max_drawdown = min(max_drawdown, drawdown)

    print(f"\nFinal Combined Portfolio Metrics:")
    print(f"CAGR: {cagr:.2%}")
    print(f"Sharpe Ratio: {sharpe:.2f}")
    print(f"Max Drawdown: {max_drawdown:.2%}")


def main():
    sector = "energy"
    pe_path = "../data/monthly_pe.json"
    sector_path = "../data/sector_average_pe.json"
    close_path = "../data/monthly_close.json"

    with open(pe_path) as f:
        pe_all = json.load(f)
    with open(sector_path) as f:
        sector_avg_pe = json.load(f)[sector]
    with open(close_path) as f:
        close_all = json.load(f)
    
    portfolio = backtest(pe_all, sector_avg_pe, close_all, sector)
    calculate_metrics(portfolio)

if __name__ == "__main__":
    main()