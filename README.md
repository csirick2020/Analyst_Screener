<h1 align="center"><b>📊 S&P500 Analyst Screener</b></h1>

---

<b>A professional analyst screener with a styled terminal interface that returns analyst upgrades for any specified trading date across all S&P500 stocks.</b>

---

## 🚀 Features

- **📅 Custom Date Input**: Enter any date in MM-DD-YYYY format to check analyst activity
- **🏛️ Trading Day Validation**: Automatically validates against US stock market holidays and weekends
- **🎨 Styled Terminal Interface**: Professional curses-based UI with color coding and visual indicators
- **📈 Real-time Progress**: Live progress tracking while processing all S&P500 stocks
- **🔍 Smart Filtering**: Shows only positive analyst actions (upgrades and initiations to Buy/Outperform/Overweight)

---

## 🛠️ How It Works

The `sp500_ticker_retrieval.py` script uses the requests module and BeautifulSoup4 to scrape a regularly maintained Wikipedia page for all 503 tickers. It then "pickles" that list (storing it on your computer) with the option to update the data as S&P500 holdings change over time.

The main `sp500_analyst_module.py` script imports this functionality and uses a for loop to make yfinance.Ticker() calls, accessing the upgrades_downgrades attribute of each ticker symbol. The program filters results to show only upgrades or coverage initiations rated as 'Buy', 'Outperform', or 'Overweight'.

### 🎯 Enhanced User Experience

- **Interactive Date Selection**: Input any date in MM-DD-YYYY format
- **Smart Validation**: Prevents checking weekends, holidays, and future dates
- **Color-Coded Output**: 
  - 🟢 Green for positive analyst actions
  - 🔵 Cyan for headers and titles
  - 🟡 Yellow for ticker symbols
  - 🟣 Magenta for analyst firm names
  - 🔴 Red for errors
- **Professional Layout**: Centered headers, progress indicators, and pagination

## 🚦 Usage

1. **Run the program**:
   ```bash
   cd src/
   python sp500_analyst_module.py
   ```

2. **Enter a date**: When prompted, enter a date in MM-DD-YYYY format (e.g., `08-15-2024`)

3. **View results**: The program will display any positive analyst actions for that trading day with:
   - 📈 Upgrades with grade changes (e.g., "Hold → Buy")
   - 🆕 New coverage initiations
   - Analyst firm names and target grades

## 📋 Requirements

- Python 3.x
- yfinance
- pandas
- requests
- beautifulsoup4
- curses (included with Python)

Install dependencies:
```bash
pip install -r requirements.txt
```

---

<b>*Please be informed that use of this program does not constitute financial advice and is intended for research purposes only.*</b>

---

This work is licensed under the [MIT License](https://github.com/csirick2020/Analyst_Screener/blob/main/LICENSE)
