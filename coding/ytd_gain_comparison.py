# filename: ytd_gain_comparison.py

import datetime
import yfinance as yf

def calculate_ytd_gain(ticker):
    # Get today's date
    today = datetime.date.today()
    start_of_year = datetime.date(today.year, 1, 1)
    
    # Fetch stock data
    stock_data = yf.download(ticker, start=start_of_year, end=today + datetime.timedelta(days=1))
    
    if stock_data.empty:
        print(f"Failed to fetch data for {ticker}.")
        return None
    
    # Ensure the data is not empty and access the first and last rows safely
    try:
        start_price = stock_data['Open'].iloc[0]  # Extract the first opening price as a scalar
        latest_price = stock_data['Close'].iloc[-1]  # Extract the last closing price as a scalar
    except IndexError:
        print(f"Insufficient data for {ticker}.")
        return None
    
    # Calculate YTD gain
    ytd_gain = ((latest_price - start_price) / start_price) * 100
    return float(ytd_gain)  # Ensure the result is a float

# Calculate YTD gains for META and TSLA
meta_ytd_gain = calculate_ytd_gain("META")
tesla_ytd_gain = calculate_ytd_gain("TSLA")

# Compare and print the results
if meta_ytd_gain is not None and tesla_ytd_gain is not None:
    print(f"Year-to-date gain for META: {meta_ytd_gain:.2f}%")
    print(f"Year-to-date gain for TESLA: {tesla_ytd_gain:.2f}%")
    
    if meta_ytd_gain > tesla_ytd_gain:
        print("META has a higher YTD gain than TESLA.")
    elif meta_ytd_gain < tesla_ytd_gain:
        print("TESLA has a higher YTD gain than META.")
    else:
        print("META and TESLA have the same YTD gain.")