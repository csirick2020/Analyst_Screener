# Script to automate retrieval of a (Pythonic) list of the S&P500 Tickers
import bs4 as bs  # BeautifulSoup4
import pickle
import requests

# Function to retrieve data from webpage and turn into BeautifulSoup object
def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})  # wikitable sortable comes from viewing the source code in browser

    # Iterate through the table to create list of tickers
    tickers = []
    for row in table.findAll('tr')[1:]:  # For each row after the header row (hence the [1:])
        ticker = row.findAll('td')[0].text  # Grab the text of the table data ('td')
        tickers.append(ticker)  # Append that text (each ticker) to the tickers list

    # Pickle the list for reusability
    # Be sure to update this list (by running the full code) periodically for changes in S&P holdings!
    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    return tickers

# save_sp500_tickers()

# Create a function which either updates the list or uses our pickle based on our choice
def get_data_from_yahoo(reload_sp500=False):  # Set this to True to update
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("/home/name01/sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    # Clean up the data for yfinance.Tickers() method
    ticker_symbols = ' '.join([ticker.strip().lower() for ticker in tickers])
    return ticker_symbols


# View the ticker list
if __name__ == "__main__":
    print(get_data_from_yahoo())
    print(type(get_data_from_yahoo()))
