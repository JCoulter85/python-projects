# Step 1: Import the yfinance library.
# This library helps us fetch historical stock market data directly from Yahoo Finance.
import yfinance as yf

# Step 2: Define the ticker symbol for the company you want to analyze.
# A ticker symbol is the unique identifier for a company's stock (e.g., "LMT" for Lockheed Martin).
ticker = "LMT"

# Step 3: Create a Ticker object.
# This object allows us to interact with the stock's data.
stock = yf.Ticker(ticker)

# Step 4: Fetch basic stock information.
# The "info" method gives us details about the company.
stock_info = stock.info

# Step 5: Fetch historical market data for the past 1 year.
# The "history" method retrieves data like opening/closing prices, volume, etc.
data = stock.history(period="1y")

# Step 6: Display the company's name and ticker symbol.
print(f"Stock Analysis for: {stock_info.get('shortName', 'Unknown Company')} ({ticker})\n")

# Step 7: Print the first few rows of the data to see what we have.
print("Historical Data (Last 5 Days):")
print(data.head())
