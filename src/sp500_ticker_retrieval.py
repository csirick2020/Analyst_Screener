# Script to automate retrieval of a (Pythonic) list of the S&P500 Tickers
import bs4 as bs  # BeautifulSoup4
import pickle
import requests

# Function to retrieve data from webpage and turn into BeautifulSoup object
def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'id': 'constituents'})  # more precise than class matching
    tickers = []

    for row in table.find_all('tr')[1:]:  # skip the header row
        tds = row.find_all('td')
        if tds:
            ticker = tds[0].text.strip()
            tickers.append(ticker)

    # Pickle the list for reusability
    # Be sure to update this list periodically for changes in S&P holdings!
    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    print("Ticker list updated...")
    print()

    return tickers


# Create a function which either updates the list or uses our pickled version based on our choice
def load_sp500_tickers(auto_update=True):  # Setting this to True auto-updates the list on every execution
    if auto_update:
        save_sp500_tickers()
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)
    # Clean up the data for yfinance.Tickers() method
    ticker_symbols = ' '.join([ticker.strip().lower() for ticker in tickers])
    return ticker_symbols


if __name__ == "__main__":
    # View the ticker list
    print(load_sp500_tickers())
