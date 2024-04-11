<h1 align="center"><b>S&P500 Analyst Screener</b></h1>

---

<b>This is a simple analyst screener that returns analyst upgrades for a specified date for all S&P500 stocks.</b>

---

The sp500_ticker_retrieval.py script uses the requests module and BeautifulSoup4 to scrape a regularly maintained Wikipedia page for all 503 tickers. It then "pickles" that list (storing it on your computer).  
The next function includes the option to update the data (because S&P500 holdings change from time to time) or use the previously "pickled" data and then formats it to be passed into yfinance.Ticker() calls.

---

From there, we import that functionality to the sp500_analyst_module.py script which uses a for loop to make yfinance.Ticker() calls and access the upgrades_downgrades attribute of each ticker symbol.  
In my code, I have chosen to filter the results by viewing only the previous day's upgrades (or coverage intiations) and only if those upgrades (or coverage initiations) are equal to 'Buy', 'Outperform', or 'Overweight'.

---

*Please be informed that use of this program does not constitute financial advice (from me), and is intended for research purposes only.*

---

<div style="text-align:center;">
    <img src="https://github.com/csirick2020/Analyst_Screener/blob/main/Analyst_Screener.S%26P500.jpg" alt="JPG of program output...">
</div>

---

This work is licensed under the [MIT License](https://github.com/csirick2020/Analyst_Screener/blob/main/LICENSE)
