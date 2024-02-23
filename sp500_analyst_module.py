# Analyst Screener (S&P 500)
import bs4 as bs  # BeautifulSoup4
import pickle
import requests
import pandas as pd
import datetime
import yfinance as yf
from sp500_ticker_retrieval import save_sp500_tickers, get_data_from_yahoo

# Get the formatted list of S&P500 tickers
ticker_list = get_data_from_yahoo()

# Replace '.' with '-' in each ticker symbol (that has a dot)
ticker_list_hyphenated = [symbol.replace('.', '-') for symbol in ticker_list.split()]

# Create a Tickers object with all ticker symbols
sp500_data = yf.Tickers(' '.join(ticker_list_hyphenated))

# Extract ticker symbols from the Tickers object
tick_symbols = list(sp500_data.tickers.keys())

print("Retrieving yesterday's analyst data for S&P500 stocks:")
print()
# Iterate through each ticker symbol and access its data
for symbol in tick_symbols:
    ticky = sp500_data.tickers[symbol]
    actions = ticky.upgrades_downgrades
    # Get the current date and calculate the date for the previous day
    current_date = datetime.date.today()
    previous_date = current_date - datetime.timedelta(days=1)
    # Filter the DataFrame for entries from the previous day
    previous_day_actions = actions[actions.index.date == previous_date]
    # Do not print empty DataFrames (for tickers without analyst activity)
    if not previous_day_actions.empty:
        # Filter the DataFrame based on multiple conditions
        filtered_actions = previous_day_actions[(previous_day_actions['Action'].isin(['up', 'init'])) &
                                                (previous_day_actions['ToGrade'].isin(['Buy', 'Outperform', 'Overweight']))]
        if not filtered_actions.empty:
            # Print the filtered DataFrame
            print(f"Analyst action(s) for {symbol.upper()} on {previous_date}:")
            print(filtered_actions)
            print()
