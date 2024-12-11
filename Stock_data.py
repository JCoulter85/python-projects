# Step 1: Import the necessary library.
import yfinance as yf

# Step 2: Define a list of ticker symbols for multiple companies.
tickers = [
    "LMT", "RTX", "NOC", "BA", "BLK", 
    "GD", "BAESY", "HO.PA", "FINMY", "SAABF", 
    "RNMBY", "HII", "KTOS", "AVAV", "LHX", "TXT"
]

# Step 3: Loop through each ticker symbol in the list.
for ticker in tickers:
    # Step 4: Create a Ticker object for the current stock.
    stock = yf.Ticker(ticker)

    # Step 5: Fetch basic stock information and historical data.
    stock_info = stock.info

    # Use period="5d" and interval="1d" to fetch only the last 5 trading days.
    data = stock.history(period="5d", interval="1d")

    # Check if data is available before proceeding.
    if data.empty:
        print(f"No recent data available for {ticker}. Skipping...\n")
        continue

    # Step 6: Extract key metrics from the stock information.
    current_price = stock_info.get('currentPrice', 'N/A')
    fifty_two_week_high = stock_info.get('fiftyTwoWeekHigh', 'N/A')
    fifty_two_week_low = stock_info.get('fiftyTwoWeekLow', 'N/A')
    average_volume = stock_info.get('averageVolume', 'N/A')
    sector = stock_info.get('sector', 'N/A')  # Define sector here

    # Step 7: Display the company's name, ticker symbol, and key metrics.
    print(f"\nStock Analysis for: {stock_info.get('shortName', 'Unknown Company')} ({ticker})")
    print(f"Sector: {sector}")  # Use the sector variable here
    print(f"Current Price: ${current_price}")
    print(f"52-Week High: ${fifty_two_week_high}")
    print(f"52-Week Low: ${fifty_two_week_low}")
    print(f"Average Volume: {average_volume} shares/day")

    # Step 8: Print the most recent 5 rows of historical data for this stock.
    print("\nHistorical Data (Most Recent 5 Days):")
    print(data)  # Show the fetched data
    print("-" * 50)  # Separator for readability