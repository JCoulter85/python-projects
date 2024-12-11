# Step 1: Import the yfinance library.
# This library helps us fetch historical stock market data directly from Yahoo Finance.
import yfinance as yf

# Step 2: Define a list of ticker symbols for multiple companies.
# These are some examples of military and defense-focused companies.
tickers = ["LMT", "RTX", "NOC", "BA", "BLK"]

# Step 3: Loop through each ticker symbol in the list.
for ticker in tickers:
    # Step 4: Create a Ticker object for the current stock.
    stock = yf.Ticker(ticker)

    # Step 5: Fetch basic stock information.
    stock_info = stock.info
    
    # Step 6: Fetch historical market data for the past 1 year.
    data = stock.history(period="1y")

 # Step 7: Display the company's name and ticker symbol.
    # Use the .get() method to safely access the company's name from stock_info.
    print(f"\nStock Analysis for: {stock_info.get('shortName', 'Unknown Company')} ({ticker})")

    # Step 8: Print the first few rows of historical data for this stock.
    print("Historical Data (Last 5 Days):")
    print(data.head())
    print("-" * 50)  # Separator for readability.