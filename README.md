<h1 align="center"><b>S&P500 Analyst Screener</b></h1>

---
This is a simple analyst screener that returns analyst upgrades for a specified date for all S&P500 stocks. The sp500_ticker_retrieval.py script uses the requests module and BeautifulSoup4 to scrape a regularly maintained Wikipedia page for all 503 tickers. It then "pickles" that list (storing it on your computer). The next function includes the option to update the data (because S&P500 holdings change from time to time) or use the previously "pickled" data and then formats it to be passed into a yfinance.Tickers() call. From there, we import that functionality to the sp500_analyst_module.py script, which provides a little bit more formatting, creates the yfinance.Tickers() object, and then converts the ticker symbols into an iterable list object. Lastly, we use a for loop to call the upgrades_downgrades method (or attribute?) on each ticker symbol and filter by our criteria. In this case, I have chosen to view the previous day's upgrades (or coverage intiations) only, and only if those upgrades (or coverage initiations) are equal to 'Buy', 'Outperform', or 'Overweight'.
---
*Please be informed that use of this program does not constitute financial advice (from me), and is intended for research purposes only.*
---
<div style="text-align:center;">
    <img src="https://github.com/csirick2020/Analyst_Screener/blob/main/Analyst_Screener.S%26P500.jpg" alt="JPG of program output...">
</div>

