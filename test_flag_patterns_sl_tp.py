import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
from flags_pennants import find_flags_pennants_pips, find_flags_pennants_trendline

data = pd.read_csv('EURUSD_1m_past_7_days.csv', parse_dates=['date'])
# data['date'] = data['date'].astype('datetime64[s]')
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

point = 0.0000000000000001
lot = 0.1
deviation = 20

for order in orders:
    bull_flags, bear_flags, bull_pennants, bear_pennants = find_flags_pennants_pips(dat_slice, order)

    bull_flag_df = pd.DataFrame()
    bull_pennant_df = pd.DataFrame()
    bear_flag_df = pd.DataFrame()
    bear_pennant_df = pd.DataFrame()

    for pattern_type, pattern_list, df in [("bull_flag", bull_flags, bull_flag_df),
                                           ("bear_flag", bear_flags, bear_flag_df),
                                           ("bull_pennant", bull_pennants, bull_pennant_df),
                                           ("bear_pennant", bear_pennants, bear_pennant_df)]:
        for i, pattern in enumerate(pattern_list):
            df.loc[i, 'flag_width'] = pattern.flag_width
            df.loc[i, 'flag_height'] = pattern.flag_height
            df.loc[i, 'pole_width'] = pattern.pole_width
            df.loc[i, 'pole_height'] = pattern.pole_height
            df.loc[i, 'slope'] = pattern.resist_slope

            sl_pips = int(pattern.flag_width) * 10
            tp_pips = int(pattern.flag_width * 2) * 10

            if "bull" in pattern_type:
                trade_type = 'buy'
                sl = pattern.conf_y - sl_pips * point
                tp = pattern.conf_y + tp_pips * point
            else:
                trade_type = 'sell'
                sl = pattern.conf_y + sl_pips * point
                tp = pattern.conf_y - tp_pips * point

            hit_sl = False
            hit_tp = False

            for j in range(pattern.conf_x + 1, len(dat_slice)):
                price = dat_slice[j]
                if (trade_type == 'buy' and price <= sl) or (trade_type == 'sell' and price >= sl):
                    hit_sl = True
                    break
                if (trade_type == 'buy' and price >= tp) or (trade_type == 'sell' and price <= tp):
                    hit_tp = True
                    break

            if hit_tp:
                df.loc[i, 'return'] = tp - pattern.conf_y if trade_type == 'buy' else pattern.conf_y - tp
                df.loc[i, 'win'] = True
            elif hit_sl:
                df.loc[i, 'return'] = sl - pattern.conf_y if trade_type == 'buy' else pattern.conf_y - sl
                df.loc[i, 'win'] = False
            else:
                df.loc[i, 'return'] = np.nan
                df.loc[i, 'win'] = np.nan

    # skip empty dataframes
    if bull_flag_df.empty:
        bull_flag_wr.append(np.nan)
        bull_flag_avg.append(np.nan)
        bull_flag_count.append(0)
        bull_flag_total_ret.append(0)
    else:
        bull_flag_wr.append(bull_flag_df['win'].mean())
        bull_flag_avg.append(bull_flag_df['return'].mean())
        bull_flag_count.append(bull_flag_df.shape[0])
        bull_flag_total_ret.append(bull_flag_df['return'].sum())
        
    if bull_pennant_df.empty:
        bull_pennant_wr.append(np.nan)
        bull_pennant_avg.append(np.nan)
        bull_pennant_count.append(0)
        bull_pennant_total_ret.append(0)
    else:
        bull_pennant_wr.append(bull_pennant_df['win'].mean())
        bull_pennant_avg.append(bull_pennant_df['return'].mean())
        bull_pennant_count.append(bull_pennant_df.shape[0])
        bull_pennant_total_ret.append(bull_pennant_df['return'].sum())
        
    if bear_flag_df.empty:
        bear_flag_wr.append(np.nan)
        bear_flag_avg.append(np.nan)
        bear_flag_count.append(0)
        bear_flag_total_ret.append(0)
    else:
        bear_flag_wr.append(bear_flag_df['win'].mean())
        bear_flag_avg.append(bear_flag_df['return'].mean())
        bear_flag_count.append(bear_flag_df.shape[0])
        bear_flag_total_ret.append(bear_flag_df['return'].sum())
        
    if bear_pennant_df.empty:
        bear_pennant_wr.append(np.nan)
        bear_pennant_avg.append(np.nan)
        bear_pennant_count.append(0)
        bear_pennant_total_ret.append(0)
    else:
        bear_pennant_wr.append(bear_pennant_df['win'].mean())
        bear_pennant_avg.append(bear_pennant_df['return'].mean())
        bear_pennant_count.append(bear_pennant_df.shape[0])
        bear_pennant_total_ret.append(bear_pennant_df['return'].sum())

results_df = pd.DataFrame({
    'order': orders,
    'bull_flag_wr': bull_flag_wr,
    'bull_pennant_wr': bull_pennant_wr,
    'bear_flag_wr': bear_flag_wr,
    'bear_pennant_wr': bear_pennant_wr,
    'bull_flag_avg': bull_flag_avg,
    'bull_pennant_avg': bull_pennant_avg,
    'bear_flag_avg': bear_flag_avg,
    'bear_pennant_avg': bear_pennant_avg,
    'bull_flag_count': bull_flag_count,
    'bull_pennant_count': bull_pennant_count,
    'bear_flag_count': bear_flag_count,
    'bear_pennant_count': bear_pennant_count,
    'bull_flag_total': bull_flag_total_ret,
    'bull_pennant_total': bull_pennant_total_ret,
    'bear_flag_total': bear_flag_total_ret,
    'bear_pennant_total': bear_pennant_total_ret
})

results_df.set_index('order', inplace=True)

fig, ax = plt.subplots(2, 2)
fig.suptitle("Bull Flag Performance", fontsize=20)
results_df['bull_flag_count'].plot.bar(ax=ax[0,0])
results_df['bull_flag_avg'].plot.bar(ax=ax[0,1], color='yellow')
results_df['bull_flag_total'].plot.bar(ax=ax[1,0], color='green')
results_df['bull_flag_wr'].plot.bar(ax=ax[1,1], color='orange')
ax[0,1].hlines(0.0, xmin=-1, xmax=len(orders), color='white')
ax[1,0].hlines(0.0, xmin=-1, xmax=len(orders), color='white')
ax[1,1].hlines(0.5, xmin=-1, xmax=len(orders), color='white')
ax[0,0].set_title('Number of Patterns Found')
ax[0,0].set_xlabel('Order Parameter')
ax[0,0].set_ylabel('Number of Patterns')
ax[0,1].set_title('Average Pattern Return')
ax[0,1].set_xlabel('Order Parameter')
ax[0,1].set_ylabel('Average Log Return')
ax[1,0].set_title('Sum of Returns')
ax[1,0].set_xlabel('Order Parameter')
ax[1,0].set_ylabel('Total Log Return')
ax[1,1].set_title('Win Rate')
ax[1,1].set_xlabel('Order Parameter')
ax[1,1].set_ylabel('Win Rate Percentage')
plt.show()

fig, ax = plt.subplots(2, 2)
fig.suptitle("Bear Flag Performance", fontsize=20)
results_df['bear_flag_count'].plot.bar(ax=ax[0,0])
results_df['bear_flag_avg'].plot.bar(ax=ax[0,1], color='yellow')
results_df['bear_flag_total'].plot.bar(ax=ax[1,0], color='green')
results_df['bear_flag_wr'].plot.bar(ax=ax[1,1], color='orange')
ax[0,1].hlines(0.0, xmin=-1, xmax=len(orders), color='white')
ax[1,0].hlines(0.0, xmin=-1, xmax=len(orders), color='white')
ax[1,1].hlines(0.5, xmin=-1, xmax=len(orders), color='white')
ax[0,0].set_title('Number of Patterns Found')
ax[0,0].set_xlabel('Order Parameter')
ax[0,0].set_ylabel('Number of Patterns')
ax[0,1].set_title('Average Pattern Return')
ax[0,1].set_xlabel('Order Parameter')
ax[0,1].set_ylabel('Average Log Return')
ax[1,0].set_title('Sum of Returns')
ax[1,0].set_xlabel('Order Parameter')
ax[1,0].set_ylabel('Total Log Return')
ax[1,1].set_title('Win Rate')
ax[1,1].set_xlabel('Order Parameter')
ax[1,1].set_ylabel('Win Rate Percentage')
plt.show()

fig, ax = plt.subplots(2, 2)
fig.suptitle("Bull Pennant Performance", fontsize=20)
results_df['bull_pennant_count'].plot.bar(ax=ax[0,0])
results_df['bull_pennant_avg'].plot.bar(ax=ax[0,1], color='yellow')
results_df['bull_pennant_total'].plot.bar(ax=ax[1,0], color='green')
results_df['bull_pennant_wr'].plot.bar(ax=ax[1,1], color='orange')
ax[0,1].hlines(0.0, xmin=-1, xmax=len(orders), color='white')
ax[1,0].hlines(0.0, xmin=-1, xmax=len(orders), color='white')
ax[1,1].hlines(0.5, xmin=-1, xmax=len(orders), color='white')
ax[0,0].set_title('Number of Patterns Found')
ax[0,0].set_xlabel('Order Parameter')
ax[0,0].set_ylabel('Number of Patterns')
ax[0,1].set_title('Average Pattern Return')
ax[0,1].set_xlabel('Order Parameter')
ax[0,1].set_ylabel('Average Log Return')
ax[1,0].set_title('Sum of Returns')
ax[1,0].set_xlabel('Order Parameter')
ax[1,0].set_ylabel('Total Log Return')
ax[1,1].set_title('Win Rate')
ax[1,1].set_xlabel('Order Parameter')
ax[1,1].set_ylabel('Win Rate Percentage')
plt.show()

fig, ax = plt.subplots(2, 2)
fig.suptitle("Bear Pennant Performance", fontsize=20)
results_df['bear_pennant_count'].plot.bar(ax=ax[0,0])
results_df['bear_pennant_avg'].plot.bar(ax=ax[0,1], color='yellow')
results_df['bear_pennant_total'].plot.bar(ax=ax[1,0], color='green')
results_df['bear_pennant_wr'].plot.bar(ax=ax[1,1], color='orange')
ax[0,1].hlines(0.0, xmin=-1, xmax=len(orders), color='white')
ax[1,0].hlines(0.0, xmin=-1, xmax=len(orders), color='white')
ax[1,1].hlines(0.5, xmin=-1, xmax=len(orders), color='white')
ax[0,0].set_title('Number of Patterns Found')
ax[0,0].set_xlabel('Order Parameter')
ax[0,0].set_ylabel('Number of Patterns')
ax[0,1].set_title('Average Pattern Return')
ax[0,1].set_xlabel('Order Parameter')
ax[0,1].set_ylabel('Average Log Return')
ax[1,0].set_title('Sum of Returns')
ax[1,0].set_xlabel('Order Parameter')
ax[1,0].set_ylabel('Total Log Return')
ax[1,1].set_title('Win Rate')
ax[1,1].set_xlabel('Order Parameter')
ax[1,1].set_ylabel('Win Rate Percentage')
plt.show()

# Export results DataFrame to CSV
results_df.to_csv('results/results_summary.csv')
