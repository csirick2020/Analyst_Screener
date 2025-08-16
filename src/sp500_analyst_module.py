# Analyst Screener (S&P 500)
import datetime
import yfinance as yf
import pandas as pd
import curses
import re
from sp500_ticker_retrieval import load_sp500_tickers

# Get the formatted list of S&P500 tickers
ticker_list = load_sp500_tickers()

# Replace '.' with '-' in each ticker symbol
ticker_list_hyphenated = [symbol.upper().replace('.', '-') for symbol in ticker_list.split()]

# Create a Tickers object with all ticker symbols
sp500_data = yf.Tickers(' '.join(ticker_list_hyphenated))

def is_trading_day(date_obj):
    """Check if a given date is a US stock market trading day"""
    # Check if it's a weekend
    if date_obj.weekday() >= 5:  # Saturday = 5, Sunday = 6
        return False
    
    # Check for major US holidays (simplified list of market closures)
    year = date_obj.year
    
    # New Year's Day
    if date_obj.month == 1 and date_obj.day == 1:
        return False
    
    # Martin Luther King Jr. Day (3rd Monday in January)
    mlk_day = datetime.date(year, 1, 1)
    while mlk_day.weekday() != 0:  # Find first Monday
        mlk_day += datetime.timedelta(days=1)
    mlk_day += datetime.timedelta(days=14)  # 3rd Monday
    if date_obj == mlk_day:
        return False
    
    # Presidents Day (3rd Monday in February)
    pres_day = datetime.date(year, 2, 1)
    while pres_day.weekday() != 0:
        pres_day += datetime.timedelta(days=1)
    pres_day += datetime.timedelta(days=14)
    if date_obj == pres_day:
        return False
    
    # Memorial Day (last Monday in May)
    memorial_day = datetime.date(year, 5, 31)
    while memorial_day.weekday() != 0:
        memorial_day -= datetime.timedelta(days=1)
    if date_obj == memorial_day:
        return False
    
    # Independence Day (July 4th, or observed date)
    july_4 = datetime.date(year, 7, 4)
    if july_4.weekday() == 5:  # Saturday
        july_4 -= datetime.timedelta(days=1)  # Friday
    elif july_4.weekday() == 6:  # Sunday
        july_4 += datetime.timedelta(days=1)  # Monday
    if date_obj == july_4:
        return False
    
    # Labor Day (1st Monday in September)
    labor_day = datetime.date(year, 9, 1)
    while labor_day.weekday() != 0:
        labor_day += datetime.timedelta(days=1)
    if date_obj == labor_day:
        return False
    
    # Thanksgiving (4th Thursday in November)
    thanksgiving = datetime.date(year, 11, 1)
    while thanksgiving.weekday() != 3:  # Thursday
        thanksgiving += datetime.timedelta(days=1)
    thanksgiving += datetime.timedelta(days=21)  # 4th Thursday
    if date_obj == thanksgiving:
        return False
    
    # Christmas Day (December 25th, or observed date)
    christmas = datetime.date(year, 12, 25)
    if christmas.weekday() == 5:  # Saturday
        christmas -= datetime.timedelta(days=1)  # Friday
    elif christmas.weekday() == 6:  # Sunday
        christmas += datetime.timedelta(days=1)  # Monday
    if date_obj == christmas:
        return False
    
    return True

def parse_date_input(date_string):
    """Parse MM-DD-YYYY format and return date object"""
    try:
        # Validate format with regex
        if not re.match(r'^\d{2}-\d{2}-\d{4}$', date_string):
            return None, "Invalid format. Please use MM-DD-YYYY format."
        
        # Parse the date
        month, day, year = map(int, date_string.split('-'))
        date_obj = datetime.date(year, month, day)
        
        # Check if it's a future date
        if date_obj > datetime.date.today():
            return None, "Cannot check future dates."
        
        # Check if it's a trading day
        if not is_trading_day(date_obj):
            day_name = date_obj.strftime("%A")
            return None, f"{date_obj.strftime('%B %d, %Y')} ({day_name}) was not a trading day."
        
        return date_obj, None
        
    except ValueError as e:
        return None, f"Invalid date: {str(e)}"

def init_colors():
    """Initialize color pairs for curses"""
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)    # Success/Buy
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)     # Headers
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)   # Ticker symbols
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)    # Regular text
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)      # Errors
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # Firm names

def display_header(stdscr, title, date_str):
    """Display styled header"""
    height, width = stdscr.getmaxyx()
    
    # Clear screen
    stdscr.clear()
    
    # Title
    title_text = f"📊 {title}"
    stdscr.addstr(0, (width - len(title_text)) // 2, title_text, 
                  curses.color_pair(2) | curses.A_BOLD)
    
    # Date
    date_text = f"📅 {date_str}"
    stdscr.addstr(1, (width - len(date_text)) // 2, date_text, 
                  curses.color_pair(4))
    
    # Separator line
    separator = "═" * (width - 4)
    stdscr.addstr(2, 2, separator, curses.color_pair(2))
    
    stdscr.refresh()
    return 4  # Return starting line for content

def display_analyst_data(stdscr, symbol, filtered_actions, current_line):
    """Display styled analyst data for a symbol"""
    height, width = stdscr.getmaxyx()
    
    if current_line >= height - 3:
        stdscr.addstr(height - 2, 2, "Press any key to continue...", 
                      curses.color_pair(4) | curses.A_BLINK)
        stdscr.refresh()
        stdscr.getch()
        stdscr.clear()
        current_line = display_header(stdscr, "S&P 500 Analyst Screener", 
                                    datetime.date.today().strftime("%B %d, %Y"))
    
    # Symbol header
    symbol_text = f"🔍 {symbol}"
    stdscr.addstr(current_line, 2, symbol_text, 
                  curses.color_pair(3) | curses.A_BOLD)
    current_line += 1
    
    # Display each action
    for _, row in filtered_actions.iterrows():
        if current_line >= height - 3:
            stdscr.addstr(height - 2, 2, "Press any key to continue...", 
                          curses.color_pair(4) | curses.A_BLINK)
            stdscr.refresh()
            stdscr.getch()
            stdscr.clear()
            current_line = display_header(stdscr, "S&P 500 Analyst Screener", 
                                        datetime.date.today().strftime("%B %d, %Y"))
        
        # Format the action info
        firm = row.get('Firm', 'N/A')
        action = row.get('Action', 'N/A')
        to_grade = row.get('ToGrade', 'N/A')
        from_grade = row.get('FromGrade', 'N/A')
        
        # Action line with colors
        action_symbol = "📈" if action == "up" else "🆕" if action == "init" else "📊"
        action_text = f"  {action_symbol} {firm}"
        stdscr.addstr(current_line, 4, action_text, curses.color_pair(6))
        current_line += 1
        
        # Grade change
        if from_grade and from_grade != 'N/A':
            grade_text = f"    {from_grade} → {to_grade}"
        else:
            grade_text = f"    Initial: {to_grade}"
        
        stdscr.addstr(current_line, 4, grade_text, curses.color_pair(1))
        current_line += 1
    
    current_line += 1  # Add spacing
    stdscr.refresh()
    return current_line

def display_error(stdscr, symbol, error, current_line):
    """Display styled error message"""
    height, width = stdscr.getmaxyx()
    
    if current_line >= height - 3:
        stdscr.addstr(height - 2, 2, "Press any key to continue...", 
                      curses.color_pair(4) | curses.A_BLINK)
        stdscr.refresh()
        stdscr.getch()
        stdscr.clear()
        current_line = display_header(stdscr, "S&P 500 Analyst Screener", 
                                    datetime.date.today().strftime("%B %d, %Y"))
    
    error_text = f"❌ Error for {symbol}: {str(error)[:60]}..."
    stdscr.addstr(current_line, 2, error_text, curses.color_pair(5))
    current_line += 2
    stdscr.refresh()
    return current_line

def get_date_input(stdscr):
    """Get date input with styled interface and validation"""
    height, width = stdscr.getmaxyx()
    
    while True:
        # Clear screen and show menu
        stdscr.clear()
        
        # Title
        title = "📊 S&P 500 Analyst Screener"
        stdscr.addstr(2, (width - len(title)) // 2, title, 
                      curses.color_pair(2) | curses.A_BOLD)
        
        # Instructions
        stdscr.addstr(5, (width - 50) // 2, "Enter the date to check for analyst activity:", 
                      curses.color_pair(4))
        stdscr.addstr(7, (width - 30) // 2, "📅 Format: MM-DD-YYYY", 
                      curses.color_pair(3))
        stdscr.addstr(8, (width - 40) // 2, "Example: 08-15-2024", 
                      curses.color_pair(4))
        
        stdscr.addstr(10, (width - 20) // 2, "Date: ", 
                      curses.color_pair(4))
        
        stdscr.refresh()
        
        # Enable cursor and echo for input
        curses.curs_set(1)
        curses.echo()
        
        # Get input
        input_y = 10
        input_x = (width - 20) // 2 + 6
        stdscr.move(input_y, input_x)
        
        try:
            date_input = stdscr.getstr(input_y, input_x, 10).decode('utf-8')
        except:
            date_input = ""
        
        # Disable cursor and echo
        curses.curs_set(0)
        curses.noecho()
        
        # Validate the input
        if date_input:
            date_obj, error_msg = parse_date_input(date_input)
            
            if date_obj:
                return date_obj
            else:
                # Show error message
                stdscr.addstr(12, (width - len(error_msg)) // 2, error_msg, 
                              curses.color_pair(5) | curses.A_BOLD)
                stdscr.addstr(14, (width - 30) // 2, "Press any key to try again...", 
                              curses.color_pair(4))
                stdscr.refresh()
                stdscr.getch()
        else:
            # Show error for empty input
            error_msg = "Please enter a date."
            stdscr.addstr(12, (width - len(error_msg)) // 2, error_msg, 
                          curses.color_pair(5) | curses.A_BOLD)
            stdscr.addstr(14, (width - 30) // 2, "Press any key to try again...", 
                          curses.color_pair(4))
            stdscr.refresh()
            stdscr.getch()

def main_curses(stdscr):
    """Main function with curses interface"""
    # Initialize colors
    init_colors()
    curses.curs_set(0)  # Hide cursor
    
    # Get date input from user
    selected_date = get_date_input(stdscr)
    
    # Display header with selected date
    date_str = selected_date.strftime("%B %d, %Y")
    current_line = display_header(stdscr, f"Checking analyst data for {date_str}", date_str)
    
    # Progress indicator
    total_tickers = len(ticker_list_hyphenated)
    processed = 0
    
    # Process each ticker
    for symbol in ticker_list_hyphenated:
        processed += 1
        
        # Update progress in bottom right
        height, width = stdscr.getmaxyx()
        progress_text = f"Progress: {processed}/{total_tickers}"
        stdscr.addstr(height - 1, width - len(progress_text) - 2, progress_text, 
                      curses.color_pair(4))
        stdscr.refresh()
        
        try:
            ticky = sp500_data.tickers[symbol]
            actions = ticky.upgrades_downgrades

            # Ensure the index is a DatetimeIndex
            if not isinstance(actions.index, pd.DatetimeIndex):
                actions.index = pd.to_datetime(actions.index)

            # Filter based on selected date
            day_actions = actions[actions.index.date == selected_date]

            # Filter for positive actions only
            if not day_actions.empty:
                filtered_actions = day_actions[(day_actions['Action'].isin(['up', 'init'])) &
                                             (day_actions['ToGrade'].isin(['Buy', 'Outperform', 'Overweight']))]
                if not filtered_actions.empty:
                    current_line = display_analyst_data(stdscr, symbol, filtered_actions, current_line)

        except Exception as e:
            current_line = display_error(stdscr, symbol, e, current_line)
    
    # Final message
    height, width = stdscr.getmaxyx()
    final_text = "✅ Screening complete! Press any key to exit..."
    stdscr.addstr(height - 2, (width - len(final_text)) // 2, final_text, 
                  curses.color_pair(2) | curses.A_BLINK)
    stdscr.refresh()
    stdscr.getch()

# Run the curses application
if __name__ == "__main__":
    curses.wrapper(main_curses)
