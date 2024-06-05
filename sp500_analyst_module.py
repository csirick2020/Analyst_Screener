# Analyst Screener (S&P 500)
import datetime
import yfinance as yf
from sp500_ticker_retrieval import load_sp500_tickers

# Get the formatted list of S&P500 tickers
ticker_list = load_sp500_tickers()

# Replace '.' with '-' in each ticker symbol
ticker_list_hyphenated = [symbol.replace('.', '-') for symbol in ticker_list.split()]

# Create a Tickers object with all ticker symbols
sp500_data = yf.Tickers(' '.join(ticker_list_hyphenated))

# Extract ticker symbols from the Tickers object
tick_symbols = list(sp500_data.tickers.keys())

day_to_check = input("Would you like to check today's analyst activity or yesterday's?\n\
Enter 1 for today or 2 for yesterday: ")


if day_to_check == "1":
    # For today...
    print("Retrieving today's analyst data for S&P500 stocks:")
elif day_to_check == "2":
    # For the previous day...
    print("Retrieving yesterday's analyst data for S&P500 stocks:")
print()
# Iterate through each ticker symbol and access its data
for symbol in tick_symbols:
    ticky = sp500_data.tickers[symbol]
    actions = ticky.upgrades_downgrades
    # Get the current date and calculate the date for the previous day
    current_date = datetime.date.today()
    previous_date = current_date - datetime.timedelta(days=1)
    # Filter the DataFrame and display entries
    if day_to_check == "1":
        current_day_actions = actions[actions.index.date == current_date]
        # Do not print empty DataFrames (for tickers without analyst activity)
        if not current_day_actions.empty:
            # Filter the DataFrame based on multiple conditions
            filtered_actions = current_day_actions[(current_day_actions['Action'].isin(['up', 'init'])) &
                                                   (current_day_actions['ToGrade'].isin(['Buy', 'Outperform', 'Overweight']))]
            if not filtered_actions.empty:
                # Print the filtered DataFrame
                print(f"Analyst action(s) for {symbol.upper()} on {current_date}:")
                print(filtered_actions)
                print()
    elif day_to_check == "2":
        # Filter the DataFrame and display entries
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
