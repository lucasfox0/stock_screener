import pandas as pd
import matplotlib.pyplot as plt

def plot_equity_curve(csv_path="../data/monthly_returns.csv"):
    # load and sort
    df = pd.read_csv(csv_path, parse_dates=["month"])
    df.sort_values("month", inplace=True)

    # plot (single figure, no custom colors)
    plt.figure()
    plt.plot(df["month"], df["portfolio_value"])
    plt.xlabel("Month")
    plt.ylabel("Portfolio Value")
    plt.title("Equity Curve")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_equity_curve()
