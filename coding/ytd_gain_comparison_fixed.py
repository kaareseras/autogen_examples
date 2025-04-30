# filename: ytd_gain_comparison_fixed.py
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

# Extract the closing prices from the multi-level columns
closing_prices = data['Price']['Close']

# Get the first and last available prices for each stock
first_prices = closing_prices.iloc[0]
last_prices = closing_prices.iloc[-1]

# Step 3: Calculate YTD gain
ytd_gains = ((last_prices - first_prices) / first_prices) * 100

# Step 4: Compare the gains
for stock, gain in ytd_gains.items():
    print(f"{stock} Year-to-Date Gain: {gain:.2f}%")

better_stock = ytd_gains.idxmax()
print(f"The better performing stock YTD is: {better_stock}")