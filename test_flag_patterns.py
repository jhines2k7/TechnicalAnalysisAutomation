import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
import csv
import shutil

from flags_pennants import find_flags_pennants_pips, find_flags_pennants_trendline

def export_to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        headers = data[0].keys()  # Assuming data is a list of dictionaries
        writer.writerow(headers)
        for row in data:
            writer.writerow(row.values())    

data = pd.read_csv('EURUSD900b.csv')
data['date'] = data['date'].astype('datetime64[s]')
data = data.set_index('date')

data = np.log(data)
dat_slice = data['close'].to_numpy()


orders = list(range(3, 49))
bull_flag_wr = []
bull_pennant_wr = []
bear_flag_wr = []
bear_pennant_wr = []

bull_flag_avg = []
bull_pennant_avg = []
bear_flag_avg = []
bear_pennant_avg = []

bull_flag_count = []
bull_pennant_count = []
bear_flag_count = []
bear_pennant_count = []

bull_flag_total_ret = []
bull_pennant_total_ret = []
bear_flag_total_ret = []
bear_pennant_total_ret = []


for order in orders:
    bull_flags, bear_flags, bull_pennants, bear_pennants  = find_flags_pennants_pips(dat_slice, order)
    #bull_flags, bear_flags, bull_pennants, bear_pennants  = find_flags_pennants_trendline(dat_slice, order)

    bull_flag_df = pd.DataFrame()
    bull_pennant_df = pd.DataFrame()
    bear_flag_df = pd.DataFrame()
    bear_pennant_df = pd.DataFrame()

    # Assemble data into dataframe
    hold_mult = 1.0 # Multipler of flag width to hold for after a pattern
    for i, flag in enumerate(bull_flags):
        bull_flag_df.loc[i, 'flag_width'] = flag.flag_width
        bull_flag_df.loc[i, 'flag_height'] = flag.flag_height
        bull_flag_df.loc[i, 'pole_width'] = flag.pole_width
        bull_flag_df.loc[i, 'pole_height'] = flag.pole_height
        bull_flag_df.loc[i, 'slope'] = flag.resist_slope

        hp = int(flag.flag_width * hold_mult)
        if flag.conf_x + hp >= len(data):
            bull_flag_df.loc[i, 'return'] = np.nan
        else:
            ret = dat_slice[flag.conf_x + hp] - dat_slice[flag.conf_x]
            bull_flag_df.loc[i, 'return'] = ret 

    for i, flag in enumerate(bear_flags):
        bear_flag_df.loc[i, 'flag_width'] = flag.flag_width
        bear_flag_df.loc[i, 'flag_height'] = flag.flag_height
        bear_flag_df.loc[i, 'pole_width'] = flag.pole_width
        bear_flag_df.loc[i, 'pole_height'] = flag.pole_height
        bear_flag_df.loc[i, 'slope'] = flag.support_slope

        hp = int(flag.flag_width * hold_mult)
        if flag.conf_x + hp >= len(data):
            bear_flag_df.loc[i, 'return'] = np.nan
        else:
            ret = -1 * (dat_slice[flag.conf_x + hp] - dat_slice[flag.conf_x])
            bear_flag_df.loc[i, 'return'] = ret 

    for i, pennant in enumerate(bull_pennants):
        bull_pennant_df.loc[i, 'pennant_width'] = pennant.flag_width
        bull_pennant_df.loc[i, 'pennant_height'] = pennant.flag_height
        bull_pennant_df.loc[i, 'pole_width'] = pennant.pole_width
        bull_pennant_df.loc[i, 'pole_height'] = pennant.pole_height

        hp = int(pennant.flag_width * hold_mult)
        if pennant.conf_x + hp >= len(data):
            bull_pennant_df.loc[i, 'return'] = np.nan
        else:
            ret = dat_slice[pennant.conf_x + hp] - dat_slice[pennant.conf_x]
            bull_pennant_df.loc[i, 'return'] = ret 

    for i, pennant in enumerate(bear_pennants):
        bear_pennant_df.loc[i, 'pennant_width'] = pennant.flag_width
        bear_pennant_df.loc[i, 'pennant_height'] = pennant.flag_height
        bear_pennant_df.loc[i, 'pole_width'] = pennant.pole_width
        bear_pennant_df.loc[i, 'pole_height'] = pennant.pole_height

        hp = int(pennant.flag_width * hold_mult)
        if pennant.conf_x + hp >= len(data):
            bear_pennant_df.loc[i, 'return'] = np.nan
        else:
            ret = -1 * (dat_slice[pennant.conf_x + hp] - dat_slice[pennant.conf_x])
            bear_pennant_df.loc[i, 'return'] = ret 

    if len(bull_flag_df) > 0:
        bull_flag_count.append(len(bull_flag_df))
        bull_flag_avg.append(bull_flag_df['return'].mean())
        bull_flag_wr.append(len(bull_flag_df[bull_flag_df['return'] > 0]) / len(bull_flag_df))
        bull_flag_total_ret.append(bull_flag_df['return'].sum())
    else:
        bull_flag_count.append(0)
        bull_flag_avg.append(np.nan)
        bull_flag_wr.append(np.nan)
        bull_flag_total_ret.append(0)
    
    if len(bear_flag_df) > 0:
        bear_flag_count.append(len(bear_flag_df))
        bear_flag_avg.append(bear_flag_df['return'].mean())
        bear_flag_wr.append(len(bear_flag_df[bear_flag_df['return'] > 0]) / len(bear_flag_df))
        bear_flag_total_ret.append(bear_flag_df['return'].sum())
    else:
        bear_flag_count.append(0)
        bear_flag_avg.append(np.nan)
        bear_flag_wr.append(np.nan)
        bear_flag_total_ret.append(0)
    
    if len(bull_pennant_df) > 0:
        bull_pennant_count.append(len(bull_pennant_df))
        bull_pennant_avg.append(bull_pennant_df['return'].mean())
        bull_pennant_wr.append(len(bull_pennant_df[bull_pennant_df['return'] > 0]) / len(bull_pennant_df))
        bull_pennant_total_ret.append(bull_pennant_df['return'].sum())
    else:
        bull_pennant_count.append(0)
        bull_pennant_avg.append(np.nan)
        bull_pennant_wr.append(np.nan)
        bull_pennant_total_ret.append(0)
    
    if len(bear_pennant_df) > 0:
        bear_pennant_count.append(len(bear_pennant_df))
        bear_pennant_avg.append(bear_pennant_df['return'].mean())
        bear_pennant_wr.append(len(bear_pennant_df[bear_pennant_df['return'] > 0]) / len(bear_pennant_df))
        bear_pennant_total_ret.append(bear_pennant_df['return'].sum())
    else:
        bear_pennant_count.append(0)
        bear_pennant_avg.append(np.nan)
        bear_pennant_wr.append(np.nan)
        bear_pennant_total_ret.append(0)
    

results_df = pd.DataFrame(index=orders)
results_df['bull_flag_count'] = bull_flag_count
results_df['bull_flag_avg'] = bull_flag_avg
results_df['bull_flag_wr'] = bull_flag_wr
results_df['bull_flag_total'] = bull_flag_total_ret

results_df['bear_flag_count'] = bear_flag_count
results_df['bear_flag_avg'] = bear_flag_avg
results_df['bear_flag_wr'] = bear_flag_wr
results_df['bear_flag_total'] = bear_flag_total_ret

results_df['bull_pennant_count'] = bull_pennant_count
results_df['bull_pennant_avg'] = bull_pennant_avg
results_df['bull_pennant_wr'] = bull_pennant_wr
results_df['bull_pennant_total'] = bull_pennant_total_ret

results_df['bear_pennant_count'] = bear_pennant_count
results_df['bear_pennant_avg'] = bear_pennant_avg
results_df['bear_pennant_wr'] = bear_pennant_wr
results_df['bear_pennant_total'] = bear_pennant_total_ret

results_df = pd.DataFrame({
    'order': orders,
    'bull_flag_count': np.random.randint(50, 150, size=len(orders)),
    'bull_flag_avg': np.random.uniform(-0.01, 0.01, size=len(orders)),
    'bull_flag_total': np.random.uniform(-1, 1, size=len(orders)),
    'bull_flag_wr': np.random.uniform(0.3, 0.7, size=len(orders)),
    'bull_pennant_count': np.random.randint(50, 150, size=len(orders)),
    'bull_pennant_avg': np.random.uniform(-0.01, 0.01, size=len(orders)),
    'bull_pennant_total': np.random.uniform(-1, 1, size=len(orders)),
    'bull_pennant_wr': np.random.uniform(0.3, 0.7, size=len(orders)),
    'bear_flag_count': np.random.randint(50, 150, size=len(orders)),
    'bear_flag_avg': np.random.uniform(-0.01, 0.01, size=len(orders)),
    'bear_flag_total': np.random.uniform(-1, 1, size=len(orders)),
    'bear_flag_wr': np.random.uniform(0.3, 0.7, size=len(orders)),
    'bear_pennant_count': np.random.randint(50, 150, size=len(orders)),
    'bear_pennant_avg': np.random.uniform(-0.01, 0.01, size=len(orders)),
    'bear_pennant_total': np.random.uniform(-1, 1, size=len(orders)),
    'bear_pennant_wr': np.random.uniform(0.3, 0.7, size=len(orders))
})

# delete the plot_images folder if it exists
if os.path.exists('plot_images'):
    shutil.rmtree('plot_images')

os.makedirs('plot_images')

if os.path.exists('results'):
    shutil.rmtree('results')

# os.makedirs('results')

# Export results DataFrame to CSV
# export_to_csv(results_df, 'results/results_summary.csv')

# Plotting Bull Flag Performance
fig, ax = plt.subplots(2, 2, figsize=(20, 10))
fig.suptitle("Bull Flag Performance", fontsize=20)
# results_df['bull_flag_count'].plot.bar(ax=ax[0,0])
# results_df['bull_flag_avg'].plot.bar(ax=ax[0,1], color='yellow')
# results_df['bull_flag_total'].plot.bar(ax=ax[1,0], color='green')
# results_df['bull_flag_wr'].plot.bar(ax=ax[1,1], color='orange')

# Plotting the results with explicit x-ticks
ax[0,0].bar(orders, results_df['bull_flag_count'])
ax[0,1].bar(orders, results_df['bull_flag_avg'], color='yellow')
ax[1,0].bar(orders, results_df['bull_flag_total'], color='green')
ax[1,1].bar(orders, results_df['bull_flag_wr'], color='orange')

# Adjusting x-axis labels
for a in ax.flat:
    a.set_xlabel('Order Parameter', fontsize=12)
    a.set_xticks(orders)
    a.set_ylabel(a.get_ylabel(), fontsize=12)
    a.set_xticklabels(orders, rotation=45, ha='right', fontsize=10)

ax[0,0].set_title('Number of Patterns Found', fontsize=14)
ax[0,0].set_ylabel('Number of Patterns', fontsize=12)
ax[0,1].set_title('Average Pattern Return', fontsize=14)
ax[0,1].set_ylabel('Average Log Return', fontsize=12)
ax[1,0].set_title('Sum of Returns', fontsize=14)
ax[1,0].set_ylabel('Total Log Return', fontsize=12)
ax[1,1].set_title('Win Rate', fontsize=14)
ax[1,1].set_ylabel('Win Rate Percentage', fontsize=12)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
# save plot image
plt.savefig('plot_images/bull_flag_performance.png')
plt.show()

# Plotting Bear Flag Performance
fig, ax = plt.subplots(2, 2, figsize=(20, 10))
fig.suptitle("Bear Flag Performance", fontsize=20)
# results_df['bear_flag_count'].plot.bar(ax=ax[0,0])
# results_df['bear_flag_avg'].plot.bar(ax=ax[0,1], color='yellow')
# results_df['bear_flag_total'].plot.bar(ax=ax[1,0], color='green')
# results_df['bear_flag_wr'].plot.bar(ax=ax[1,1], color='orange')

# Plotting the results with explicit x-ticks
ax[0,0].bar(orders, results_df['bull_flag_count'])
ax[0,1].bar(orders, results_df['bull_flag_avg'], color='yellow')
ax[1,0].bar(orders, results_df['bull_flag_total'], color='green')
ax[1,1].bar(orders, results_df['bull_flag_wr'], color='orange')

# Adjusting x-axis labels
for a in ax.flat:
    a.set_xlabel('Order Parameter', fontsize=12)
    a.set_xticks(orders)
    a.set_ylabel(a.get_ylabel(), fontsize=12)
    a.set_xticklabels(orders, rotation=45, ha='right', fontsize=10)

ax[0,0].set_title('Number of Patterns Found', fontsize=14)
ax[0,0].set_ylabel('Number of Patterns', fontsize=12)
ax[0,1].set_title('Average Pattern Return', fontsize=14)
ax[0,1].set_ylabel('Average Log Return', fontsize=12)
ax[1,0].set_title('Sum of Returns', fontsize=14)
ax[1,0].set_ylabel('Total Log Return', fontsize=12)
ax[1,1].set_title('Win Rate', fontsize=14)
ax[1,1].set_ylabel('Win Rate Percentage', fontsize=12)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
# save plot image
plt.savefig('plot_images/bear_flag_performance.png')
plt.show()

# Plotting Bull Pennant Performance
fig, ax = plt.subplots(2, 2, figsize=(20, 10))
fig.suptitle("Bull Pennant Performance", fontsize=20)
# results_df['bull_pennant_count'].plot.bar(ax=ax[0,0])
# results_df['bull_pennant_avg'].plot.bar(ax=ax[0,1], color='yellow')
# results_df['bull_pennant_total'].plot.bar(ax=ax[1,0], color='green')
# results_df['bull_pennant_wr'].plot.bar(ax=ax[1,1], color='orange')

# Plotting the results with explicit x-ticks
ax[0,0].bar(orders, results_df['bull_flag_count'])
ax[0,1].bar(orders, results_df['bull_flag_avg'], color='yellow')
ax[1,0].bar(orders, results_df['bull_flag_total'], color='green')
ax[1,1].bar(orders, results_df['bull_flag_wr'], color='orange')

# Adjusting x-axis labels
for a in ax.flat:
    a.set_xlabel('Order Parameter', fontsize=12)
    a.set_xticks(orders)
    a.set_ylabel(a.get_ylabel(), fontsize=12)
    a.set_xticklabels(orders, rotation=45, ha='right', fontsize=10)

ax[0,0].set_title('Number of Patterns Found', fontsize=14)
ax[0,0].set_ylabel('Number of Patterns', fontsize=12)
ax[0,1].set_title('Average Pattern Return', fontsize=14)
ax[0,1].set_ylabel('Average Log Return', fontsize=12)
ax[1,0].set_title('Sum of Returns', fontsize=14)
ax[1,0].set_ylabel('Total Log Return', fontsize=12)
ax[1,1].set_title('Win Rate', fontsize=14)
ax[1,1].set_ylabel('Win Rate Percentage', fontsize=12)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
# save plot image
plt.savefig('plot_images/bull_pennant_performance.png')
plt.show()

# Plotting Bear Pennant Performance
fig, ax = plt.subplots(2, 2, figsize=(20, 10))
fig.suptitle("Bear Pennant Performance", fontsize=20)
# results_df['bear_pennant_count'].plot.bar(ax=ax[0,0])
# results_df['bear_pennant_avg'].plot.bar(ax=ax[0,1], color='yellow')
# results_df['bear_pennant_total'].plot.bar(ax=ax[1,0], color='green')
# results_df['bear_pennant_wr'].plot.bar(ax=ax[1,1], color='orange')

# Plotting the results with explicit x-ticks
ax[0,0].bar(orders, results_df['bull_flag_count'])
ax[0,1].bar(orders, results_df['bull_flag_avg'], color='yellow')
ax[1,0].bar(orders, results_df['bull_flag_total'], color='green')
ax[1,1].bar(orders, results_df['bull_flag_wr'], color='orange')

# Adjusting x-axis labels
for a in ax.flat:
    a.set_xlabel('Order Parameter', fontsize=12)
    a.set_xticks(orders)
    a.set_ylabel(a.get_ylabel(), fontsize=12)
    a.set_xticklabels(orders, rotation=45, ha='right', fontsize=10)

ax[0,0].set_title('Number of Patterns Found', fontsize=14)
ax[0,0].set_ylabel('Number of Patterns', fontsize=12)
ax[0,1].set_title('Average Pattern Return', fontsize=14)
ax[0,1].set_ylabel('Average Log Return', fontsize=12)
ax[1,0].set_title('Sum of Returns', fontsize=14)
ax[1,0].set_ylabel('Total Log Return', fontsize=12)
ax[1,1].set_title('Win Rate', fontsize=14)
ax[1,1].set_ylabel('Win Rate Percentage', fontsize=12)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
# save plot image
plt.savefig('plot_images/bear_pennant_performance.png')
plt.show()