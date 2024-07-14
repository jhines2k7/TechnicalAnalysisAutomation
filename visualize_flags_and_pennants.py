import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
import os
import shutil

from flags_pennants import find_flags_pennants_pips

bull_flags_zoomed = None
bear_flags_zoomed = None
bull_pennants_zoomed = None
bear_pennants_zoomed = None

def plot_patterns_zoomed(data, patterns, title, filename):
    alines = []
    labels = []
    for pattern in patterns:
        base_x = data.index[pattern.base_x]
        tip_x = data.index[pattern.tip_x]
        conf_x = data.index[pattern.conf_x]
        
        alines.append([(base_x, pattern.base_y), (tip_x, pattern.tip_y)])
        alines.append([(tip_x, pattern.tip_y), (conf_x, pattern.conf_y)])
        
        label = ('Bull Flag' if pattern.type == 'bull_flag' else 
                 'Bear Flag' if pattern.type == 'bear_flag' else 
                 'Bull Pennant' if pattern.type == 'bull_pennant' else 
                 'Bear Pennant')
        label_info = f"{label}\nBase: {base_x.date()}\nTip: {tip_x.date()}\nConf: {conf_x.date()}"
        labels.append((tip_x, pattern.tip_y, label_info))
    
    mc = mpf.make_marketcolors(up='g', down='r', inherit=True)
    s = mpf.make_mpf_style(marketcolors=mc)
    
    fig, ax = plt.subplots(figsize=(16, 10))
    mpf.plot(data, type='candle', style=s, alines=alines, ax=ax, ylabel='Price')
    
    # Print debug information
    print(f"Number of patterns detected: {len(patterns)}")
    for i, (x, y, label_info) in enumerate(labels):
        print(f"Pattern {i+1}: {label_info}")
    
    if patterns:  # Only add annotations if patterns were detected
        y_range = ax.get_ylim()[1] - ax.get_ylim()[0]
        for (x, y, label_info) in labels:
            ax.annotate(label_info, xy=(x, y), xytext=(x, y + y_range * 0.05),
                        arrowprops=dict(facecolor='black', shrink=0.05),
                        bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white"),
                        fontsize=8, color='blue')

    ax.set_title(title)
    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.close(fig)  # Close the figure to free up memory

    if not patterns:
        print(f"No patterns detected for {title}")

def plot_month(df, start_date, plot_dir):
    end_date = start_date + pd.DateOffset(months=1)
    df_zoomed = df.loc[start_date:end_date]

    # Detect flag and pennant patterns in the zoomed data
    data_zoomed = df_zoomed['close'].to_numpy()
    order = 10  # You can adjust the order as needed
    bull_flags_zoomed, bear_flags_zoomed, bull_pennants_zoomed, bear_pennants_zoomed = find_flags_pennants_pips(data_zoomed, order)
    
    print(f"Number of bull flags: {len(bull_flags_zoomed)}")
    print(f"Number of bear flags: {len(bear_flags_zoomed)}")
    print(f"Number of bull pennants: {len(bull_pennants_zoomed)}")
    print(f"Number of bear pennants: {len(bear_pennants_zoomed)}")

    # Label patterns with type
    for pattern in bull_flags_zoomed:
        pattern.type = 'bull_flag'
    for pattern in bear_flags_zoomed:
        pattern.type = 'bear_flag'
    for pattern in bull_pennants_zoomed:
        pattern.type = 'bull_pennant'
    for pattern in bear_pennants_zoomed:
        pattern.type = 'bear_pennant'

    # Plot and save the patterns
    flag_filename = os.path.join(plot_dir, f'flag_patterns_{start_date.date()}_to_{end_date.date()}.png')
    pennant_filename = os.path.join(plot_dir, f'pennant_patterns_{start_date.date()}_to_{end_date.date()}.png')
    plot_patterns_zoomed(df_zoomed, bull_flags_zoomed + bear_flags_zoomed, f'Flag Patterns ({start_date.date()} to {end_date.date()})', flag_filename)
    plot_patterns_zoomed(df_zoomed, bull_pennants_zoomed + bear_pennants_zoomed, f'Pennant Patterns ({start_date.date()} to {end_date.date()})', pennant_filename)

def plot_week(df, start_date, plot_dir):
    end_date = start_date + pd.DateOffset(weeks=1)
    df_zoomed = df.loc[start_date:end_date]

    # Detect flag and pennant patterns in the zoomed data
    data_zoomed = df_zoomed['close'].to_numpy()
    order = 10  # You can adjust the order as needed
    bull_flags_zoomed, bear_flags_zoomed, bull_pennants_zoomed, bear_pennants_zoomed = find_flags_pennants_pips(data_zoomed, order)

    print(f"Number of bull flags: {len(bull_flags_zoomed)}")
    print(f"Number of bear flags: {len(bear_flags_zoomed)}")
    print(f"Number of bull pennants: {len(bull_pennants_zoomed)}")
    print(f"Number of bear pennants: {len(bear_pennants_zoomed)}")

    # Label patterns with type
    for pattern in bull_flags_zoomed:
        pattern.type = 'bull_flag'
    for pattern in bear_flags_zoomed:
        pattern.type = 'bear_flag'
    for pattern in bull_pennants_zoomed:
        pattern.type = 'bull_pennant'
    for pattern in bear_pennants_zoomed:
        pattern.type = 'bear_pennant'

    # Plot and save the patterns
    flag_filename = os.path.join(plot_dir, f'flag_patterns_{start_date.date()}_to_{end_date.date()}.png')
    pennant_filename = os.path.join(plot_dir, f'pennant_patterns_{start_date.date()}_to_{end_date.date()}.png')
    plot_patterns_zoomed(df_zoomed, bull_flags_zoomed + bear_flags_zoomed, f'Flag Patterns ({start_date.date()} to {end_date.date()})', flag_filename)
    plot_patterns_zoomed(df_zoomed, bull_pennants_zoomed + bear_pennants_zoomed, f'Pennant Patterns ({start_date.date()} to {end_date.date()})', pennant_filename)

def main():
    # Load the BTCUSDT3600.csv file
    df = pd.read_csv('BTCUSDT3600.csv')
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # Create the plot_images directory
    plot_dir = 'plot_images'
    if os.path.exists(plot_dir):
        shutil.rmtree(plot_dir)
    os.makedirs(plot_dir)

    # Choose the plotting interval
    interval = 'weekly'  # Change to 'monthly' for monthly plots

    if interval == 'monthly':
        # Plot data for each month starting from Jan 1, 2022
        start_date = pd.Timestamp('2022-01-01')
        num_months = 6  # Change this number to generate more plots
        for i in range(num_months):
            plot_month(df, start_date, plot_dir)
            start_date += pd.DateOffset(months=1)
    elif interval == 'weekly':
        # Plot data for each week starting from Jan 1, 2022
        start_date = pd.Timestamp('2022-01-01')
        num_weeks = 26  # Change this number to generate more plots
        for i in range(num_weeks):
            plot_week(df, start_date, plot_dir)
            start_date += pd.DateOffset(weeks=1)

if __name__ == "__main__":
    main()
