# Import necessary libraries
import yfinance as yf  # Library for fetching stock data
from colorama import Fore, Style  # Library for colored terminal output
import datetime  # For logging timestamps

# Define a list of ticker symbols for the companies to analyze
tickers = [
    "LMT", "RTX", "NOC", "BA", "BLK", 
    "GD", "BAESY", "HO.PA", "FINMY", "SAABF", 
    "RNMBY", "HII", "KTOS", "AVAV", "LHX", "TXT",
    "GE", "ERJ", "EADSY", "ESLT", 
    "AM.PA", "SAF.PA", "RYCEY", "KOG.OL"
]

# Loop through each ticker symbol in the list
for ticker in tickers:
    print(f"\nAnalyzing: {ticker}")  # Inform user which stock is being analyzed
    try:
        # Create a Ticker object for the current stock
        stock = yf.Ticker(ticker)

        # Fetch stock information (general company details and statistics)
        stock_info = stock.info

        # Attempt to fetch historical data for the last 5 trading days
        try:
            data = stock.history(period="5d", interval="1d")  # Get 5-day daily data
        except ValueError:
            # Handle cases where 5-day data isn't supported and fallback to 1-month data
            print(Fore.YELLOW + f"{ticker}: '5d' period not supported. Trying '1mo'...\n" + Style.RESET_ALL)
            data = stock.history(period="1mo", interval="1d")  # Get 1-month daily data
        
        # Check if any data was returned; if not, skip this ticker
        if data.empty:
            print(Fore.RED + f"No recent data available for {ticker}. Skipping...\n" + Style.RESET_ALL)
            continue

        # Extract key metrics from the stock information dictionary
        current_price = stock_info.get('currentPrice', 'N/A') or "Data Unavailable"  # Current stock price
        fifty_two_week_high = stock_info.get('fiftyTwoWeekHigh', 'N/A') or "Data Unavailable"  # 52-week high
        fifty_two_week_low = stock_info.get('fiftyTwoWeekLow', 'N/A') or "Data Unavailable"  # 52-week low
        average_volume = stock_info.get('averageVolume', 'N/A') or "Data Unavailable"  # Average trading volume
        sector = stock_info.get('sector', 'N/A') or "Data Unavailable"  # Company sector

        # Display stock analysis in a readable and color-coded format
        print(Fore.YELLOW + f"\nStock Analysis for: {stock_info.get('shortName', 'Unknown Company')} ({ticker})" + Style.RESET_ALL)
        print(Fore.CYAN + f"Sector: {sector}" + Style.RESET_ALL)
        print(Fore.GREEN + f"Current Price: ${current_price}" + Style.RESET_ALL)
        print(Fore.BLUE + f"52-Week High: ${fifty_two_week_high}" + Style.RESET_ALL)
        print(Fore.MAGENTA + f"52-Week Low: ${fifty_two_week_low}" + Style.RESET_ALL)
        print(Fore.YELLOW + f"Average Volume: {average_volume} shares/day" + Style.RESET_ALL)

        # Display the most recent historical data (last 5 days or adjusted period)
        print(Fore.WHITE + "\nHistorical Data (Most Recent 5 Days):" + Style.RESET_ALL)
        print(data)  # Print the historical data table
        print(Fore.LIGHTBLACK_EX + "-" * 50 + Style.RESET_ALL)  # Add a separator for readability

    except Exception as e:
        # Handle unexpected errors and log them for review
        print(Fore.RED + f"{ticker}: Error fetching data ({e}). Skipping..." + Style.RESET_ALL)
        with open("error_log.txt", "a") as log_file:
            # Append error details and timestamp to the log file
            log_file.write(f"{datetime.datetime.now()} - {ticker}: {str(e)}\n")