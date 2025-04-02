import pandas as pd

# URL of Wikipedia page containing the list of S&P 500 companies
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

# Read all HTML tables from the page into a list of DataFrames, and select the first one (which contains the S&P 500 companies)
sp500_df = pd.read_html(url)[0]

# Filter the DataFrame to include only rows where the sector is "Energy" and extract their ticker ("Symbol") as a list
energy_tickers = sp500_df[sp500_df["GICS Sector"] == "Energy"]["Symbol"].tolist()

print(energy_tickers)