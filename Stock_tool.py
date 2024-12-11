import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Get stock ticker from user
ticker = input("Enter stock ticker: ").upper()
stock = yf.Ticker(ticker)
data = stock.history(period="1y")

if data.empty:
    print("No data retrieved. Please check the ticker symbol or your internet connection.")
else:
    # Calculate SMAs
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()

    # Plot and save to PDF
    with PdfPages(f"{ticker}_report.pdf") as pdf:
        plt.figure(figsize=(14, 7))
        plt.plot(data['Close'], label="Close Price")
        plt.plot(data['SMA_20'], label="20-Day SMA")
        plt.plot(data['SMA_50'], label="50-Day SMA")
        plt.legend()
        plt.title(f"{ticker} Stock Analysis")
        pdf.savefig()
        plt.close()

    print(f"Analysis completed! Check '{ticker}_report.pdf'.")