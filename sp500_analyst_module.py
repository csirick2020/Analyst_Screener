# Analyst Screener (S&P 500)
import datetime
import yfinance as yf
import pandas as pd
from sp500_ticker_retrieval import load_sp500_tickers

# Get the formatted list of S&P500 tickers
ticker_list = load_sp500_tickers()

# Replace '.' with '-' in each ticker symbol
ticker_list_hyphenated = [symbol.upper().replace('.', '-') for symbol in ticker_list.split()]

# Create a Tickers object with all ticker symbols
sp500_data = yf.Tickers(' '.join(ticker_list_hyphenated))

# Get the current date and calculate the date for the previous day
current_date = datetime.date.today()
previous_date = current_date - datetime.timedelta(days=1)

# Prompt user for input
day_to_check = input("Would you like to check today's analyst activity or yesterday's?\n\
Enter 1 for today or 2 for yesterday: ")
print()

if day_to_check == "1":
    # For today...
    print("Retrieving today's analyst data for S&P500 stocks:")
elif day_to_check == "2":
    # For the previous day...
    print("Retrieving yesterday's analyst data for S&P500 stocks:")
print()

# Iterate through each ticker symbol and access its data
for symbol in ticker_list_hyphenated:
    output_occurred = False
    try:
        ticky = sp500_data.tickers[symbol]
        actions = ticky.upgrades_downgrades

        # Ensure the index is a DatetimeIndex
        if not isinstance(actions.index, pd.DatetimeIndex):
            actions.index = pd.to_datetime(actions.index)

        # If user chose to see today's analyst activity
        if day_to_check == "1":
            current_day_actions = actions[actions.index.date == current_date]

            # Do not print empty DataFrames (for tickers without analyst activity)
            if not current_day_actions.empty:
                # Filter the DataFrame based on multiple conditions
                filtered_actions = current_day_actions[(current_day_actions['Action'].isin(['up', 'init'])) &
                                                       (current_day_actions['ToGrade'].isin(['Buy', 'Outperform', 'Overweight']))]
                if not filtered_actions.empty:
                    # Print the filtered DataFrame
                    print(f"Analyst action(s) for {symbol} on {current_date}:")
                    print(filtered_actions)
                    output_occurred = True

        # If user chose to see yesterday's analyst activity
        elif day_to_check == "2":
            previous_day_actions = actions[actions.index.date == previous_date]

            # Do not print empty DataFrames (for tickers without analyst activity)
            if not previous_day_actions.empty:
                # Filter the DataFrame based on multiple conditions
                filtered_actions = previous_day_actions[(previous_day_actions['Action'].isin(['up', 'init'])) &
                                                       (previous_day_actions['ToGrade'].isin(['Buy', 'Outperform', 'Overweight']))]
                if not filtered_actions.empty:
                    # Print the filtered DataFrame
                    print(f"Analyst action(s) for {symbol} on {previous_date}:")
                    print(filtered_actions)
                    output_occurred = True

    # Handle exceptions (general)
    except Exception as e:
        print(f"General error fetching data for {symbol}: {e}")
        output_occurred = True

    # Print a blank line before the next symbol if there was any output...
    if output_occurred:
        print()
