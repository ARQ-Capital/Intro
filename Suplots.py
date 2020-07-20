%matplotlib inline
import pandas as pd
from matplotlib import pyplot as plt

def get_data(file):
    """
    Fetch data from disk
    """
    data = pd.read_csv(file + '.csv', index_col='Date', parse_dates=['Date'])
    return data

def calc_corr(ser1, ser2, window):
    """
    Calculates correlation between two series.
    """
    ret1 = ser1.pct_change()
    ret2 = ser2.pct_change()
    corr = ret1.rolling(window).corr(ret2)
    return corr

# define how many points we intend to plot. Points in this case represent trading days
points_to_plot = 300

# go get the log return data.
data = get_data('indexes')

# rebase the 2 series to the same poin in time, starting where the plot will start
for ind in data:
    data[ind + '_rebased'] = (data[-points_to_plot:][ind].pct_change() + 1).cumprod()

# Relative strength, NDX to SP500
data['rel_str'] = data['NDX'] / data['SP500']

# Calculate 50 day rolling correlation
data['corr'] = calc_corr(data['NDX'], data['SP500'], 100)

# copy Dataframe to clipboard to paste it to Excel for inspection
data.to_clipboard()

# using head or tail to print the data from the start or the bottom
data.tail(20)

# slice the data, cut points we don't intend to plot
plot_data = data[-points_to_plot:]

# make new figure and set the size.
fig = plt.figure(figsize=(12, 8))

# First subplot:
# planning for: 3 -> 3 plots high
#               1 -> 1 plot wide,
#               1 -> this being the 1st.
ax = fig.add_subplot(311)
ax.set_title('Index Comparison')
ax.semilogy(plot_data['SP500_rebased'], linestyle='-',  label='S&P 500', linewidth=3.0)
ax.semilogy(plot_data['NDX_rebased'],   linestyle='--', label='Nasdaq', linewidth=3.0)
ax.legend()
ax.grid(False)

# Second subplot:
# planning for: 3 -> 3 plots high
#               1 -> 1 plot wide,
#               2 -> this being the 2nd.
ax = fig.add_subplot(312)
ax.plot(plot_data['rel_str'], label = 'Relative Strength Nasdaq to S&P 500', linestyle=':', linewidth=3.0)
ax.legend()
ax.grid(True)

# Third subplot:
# planning for: 3 -> 3 plots high
#               1 -> 1 plot wide,
#               3 -> this being the 3rd.
ax = fig.add_subplot(313)
ax.plot(plot_data['corr'], label='Correlation between Nasdaq and S&P 500', linestyle='-.', linewidth=3.0)
ax.legend()
ax.grid(True)

#print(data[-300:])