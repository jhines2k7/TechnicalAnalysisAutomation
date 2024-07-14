import pandas as pd
import mplfinance as mpf

# Load the BTCUSDT3600.csv file
df = pd.read_csv('BTCUSDT3600.csv')

# Convert the date column to datetime format
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Define the date range for zooming in
start_date = '2018-01-08'
end_date = '2018-01-12'
df_zoomed = df.loc[start_date:end_date]

# delete the plot images folder
import os
if os.path.exists('plot_images'):
    os.system('rm -r plot_images')

# Create a new folder to save the plot images
os.mkdir('plot_images')

# Define the plot style and save the chart
save_path = 'plot_images/candlestick_chart.png'
mpf.plot(df_zoomed, type='candle', style='charles', title='BTC/USDT Candlestick Chart with Wicks',
         ylabel='Price (USDT)', volume=False, savefig=save_path)

print(f'Chart saved to {save_path}')