# filename: inspect_yfinance_data.py
import datetime
import yfinance as yf

# Step 1: Get today's date
today = datetime.date.today()
print(f"Today's date: {today}")

# Step 2: Define the stock symbols and fetch data
stocks = ['META', 'TSLA']

# Fetch the first trading day of the year
start_of_year = datetime.date(today.year, 1, 1)

# Download stock data
data = yf.download(stocks, start=start_of_year, end=today + datetime.timedelta(days=1))

# Print the structure of the data
print("Data structure:")
print(data)