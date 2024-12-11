import yfinance as yf
import matplotlib.pyplot as plt

stock = yf.Ticker("AAPL")
data = stock.history(period="1y")
print(data.head())

data['SMA_20'] = data['Close'].rolling(window=20).mean()
data['SMA_50'] = data['Close'].rolling(window=50).mean()