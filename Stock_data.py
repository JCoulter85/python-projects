# Import necessary libraries
import yfinance as yf  # Library for fetching stock data
from colorama import init, Fore, Style  # Library for colored terminal output
import datetime  # For logging timestamps

# Initialize Colorama to handle colors in Windows CMD
init(autoreset=True)

# Initial list of ticker symbols
tickers = [
    "LMT", "RTX", "NOC", "BA", "BLK", 
    "GD", "BAESY", "HO.PA", "FINMY", "SAABF", 
    "RNMBY", "HII", "KTOS", "AVAV", "LHX", "TXT",
    "GE", "ERJ", "EADSY", "ESLT", 
    "AM.PA", "SAF.PA", "RYCEY", "KOG.OL"
]

# Function to analyze a specific ticker
def analyze_ticker(ticker):
    """
    Fetch and display detailed stock information for a specific ticker.
    """
    print(f"\nAnalyzing: {ticker}")
    try:
        # Fetch stock information and historical data
        stock = yf.Ticker(ticker)
        stock_info = stock.info
        data = stock.history(period="5d", interval="1d")

        # Check if historical data is available
        if data.empty:
            print(Fore.RED + f"No recent data available for {ticker}. Skipping...\n" + Style.RESET_ALL)
            return

        # Extract key metrics
        current_price = stock_info.get('currentPrice', 'N/A') or "Data Unavailable"
        fifty_two_week_high = stock_info.get('fiftyTwoWeekHigh', 'N/A') or "Data Unavailable"
        fifty_two_week_low = stock_info.get('fiftyTwoWeekLow', 'N/A') or "Data Unavailable"
        average_volume = stock_info.get('averageVolume', 'N/A') or "Data Unavailable"
        sector = stock_info.get('sector', 'N/A') or "Data Unavailable"

        # Display stock analysis with color coding
        print(Fore.YELLOW + f"\nStock Analysis for: {stock_info.get('shortName', 'Unknown Company')} ({ticker})" + Style.RESET_ALL)
        print(Fore.CYAN + f"Sector: {sector}" + Style.RESET_ALL)
        print(Fore.GREEN + f"Current Price: ${current_price}" + Style.RESET_ALL)
        print(Fore.BLUE + f"52-Week High: ${fifty_two_week_high}" + Style.RESET_ALL)
        print(Fore.MAGENTA + f"52-Week Low: ${fifty_two_week_low}" + Style.RESET_ALL)
        print(Fore.YELLOW + f"Average Volume: {average_volume} shares/day" + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"{ticker}: Error fetching data ({e}). Skipping..." + Style.RESET_ALL)

# Function to show all companies with basic metrics
def show_all_companies():
    """
    Display key metrics (current price, 52-week high, and 52-week low) for all companies.
    """
    print("\nShowing all companies and key metrics:\n")
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            stock_info = stock.info
            current_price = stock_info.get('currentPrice', 'N/A') or "Data Unavailable"
            fifty_two_week_high = stock_info.get('fiftyTwoWeekHigh', 'N/A') or "Data Unavailable"
            fifty_two_week_low = stock_info.get('fiftyTwoWeekLow', 'N/A') or "Data Unavailable"
            print(Fore.YELLOW + f"{ticker}: Current Price: ${current_price}, 52-Week High: ${fifty_two_week_high}, 52-Week Low: ${fifty_two_week_low}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"{ticker}: Error fetching data ({e}). Skipping..." + Style.RESET_ALL)

# Function to compare companies
def compare_companies():
    """
    Compare specific metrics (e.g., current price, 52-week high) for selected companies.
    """
    print("\nComparing companies:")
    tickers_to_compare = input("Enter the tickers you want to compare, separated by commas: ").strip().upper().split(",")
    metric = input("Choose a metric to compare (current price, 52-week high, 52-week low, average volume): ").strip().lower()
    
    comparisons = []
    for ticker in tickers_to_compare:
        ticker = ticker.strip()
        if ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                stock_info = stock.info
                value = stock_info.get({
                    "current price": "currentPrice",
                    "52-week high": "fiftyTwoWeekHigh",
                    "52-week low": "fiftyTwoWeekLow",
                    "average volume": "averageVolume"
                }[metric], 'N/A') or "Data Unavailable"
                comparisons.append((ticker, value))
            except Exception as e:
                print(Fore.RED + f"Error fetching data for {ticker}: {e}" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"Ticker {ticker} is not in the list. Please add it first." + Style.RESET_ALL)

    # Display comparisons
    print(Fore.LIGHTGREEN_EX + "\nComparison Results:" + Style.RESET_ALL)
    for ticker, value in comparisons:
        print(f"{ticker}: {metric.capitalize()} = {value}")

# Function to show the last 5 days of data for all companies
def show_last_5_days():
    """
    Display the last 5 days of historical data for all companies, including the company name and ticker.
    """
    print("\nShowing last 5 days of data for all companies:\n")
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)  # Create a Ticker object
            stock_info = stock.info  # Fetch stock info to get the company name
            company_name = stock_info.get('shortName', 'Unknown Company')  # Get the company name
            data = stock.history(period="5d", interval="1d")  # Fetch last 5 days of historical data

            if data.empty:  # Check if data is available
                print(Fore.RED + f"No recent data available for {company_name} ({ticker}). Skipping...\n" + Style.RESET_ALL)
                continue

            # Display the company name and ticker with color coding
            print(Fore.YELLOW + f"\nCompany: {company_name} ({ticker})" + Style.RESET_ALL)
            print(Style.BRIGHT + f"{data}" + Style.RESET_ALL)  # Display the 5-day historical data in lightblack
            print(Fore.LIGHTBLACK_EX + "-" * 110 + Style.RESET_ALL)  # Separator for readability

        except Exception as e:
            print(Fore.RED + f"{ticker}: Error fetching historical data ({e}). Skipping..." + Style.RESET_ALL)

# Main menu loop
while True:
    # Display current tickers
    print(Fore.LIGHTBLUE_EX + "\nCurrent Companies in the Application:" + Style.RESET_ALL)
    print(", ".join(tickers))

    # Menu options
    print(Fore.LIGHTBLUE_EX + "\nOptions:" + Style.RESET_ALL)
    print("1. Analyze a specific company")
    print("2. Add a new company")
    print("3. Remove a company")
    print("4. Show all companies")
    print("5. Compare companies")
    print("6. Show last 5 days of data for all companies")
    print("7. Exit the application")

    # Get user choice
    choice = input(Fore.LIGHTBLUE_EX + "\nEnter your choice (1-7): " + Style.RESET_ALL).strip()

    if choice == "1":
        ticker_to_analyze = input("Enter the ticker symbol of the company to analyze: ").strip().upper()
        if ticker_to_analyze in tickers:
            analyze_ticker(ticker_to_analyze)
        else:
            print(Fore.RED + "Ticker not found in the list. Please add it first." + Style.RESET_ALL)

    elif choice == "2":
        new_ticker = input("Enter the ticker symbol to add: ").strip().upper()
        if new_ticker not in tickers:
            tickers.append(new_ticker)
            print(Fore.GREEN + f"Ticker {new_ticker} added successfully!" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + f"Ticker {new_ticker} is already in the list." + Style.RESET_ALL)

    elif choice == "3":
        ticker_to_remove = input("Enter the ticker symbol to remove: ").strip().upper()
        if ticker_to_remove in tickers:
            tickers.remove(ticker_to_remove)
            print(Fore.GREEN + f"Ticker {ticker_to_remove} removed successfully!" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"Ticker {ticker_to_remove} not found in the list." + Style.RESET_ALL)

    elif choice == "4":
        show_all_companies()

    elif choice == "5":
        compare_companies()

    elif choice == "6":
        show_last_5_days()

    elif choice == "7":
        print(Fore.CYAN + "Exiting the application. Goodbye!" + Style.RESET_ALL)
        break

    else:
        print(Fore.RED + "Invalid choice. Please enter a number between 1 and 7." + Style.RESET_ALL)