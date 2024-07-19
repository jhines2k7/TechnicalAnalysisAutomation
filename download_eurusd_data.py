import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

end_date = datetime.today()
start_date = end_date - timedelta(days=6)

# Download historical data for EUR/USD
data = yf.download('EURUSD=X', start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), interval='1m')

# Lowercase all column header names
data.columns = [col.lower() for col in data.columns]

# dates are in the first column. How do I convert them from this: 
# Remove the last two columns
data = data.iloc[:, :-2]

# rearrange columns
data = data[['close', 'open', 'high', 'low']]

# Save to CSV
data.to_csv('EURUSD_1m_past_7_days.csv')

print("Data saved to EURUSD_1m_past_7_days.csv")