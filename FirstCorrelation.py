%matplotlib inline
import pandas as pd
from matplotlib import pyplot as plt

def get_returns(file):
    """
    This function get_data reads a data file frrom disk
    and returns percentage returns.
    """
    print(file)
    return pd.read_csv(file + '.csv', index_col=0, parse_dates=True).pct_change()

# Get the S&P time series from disk
df = get_returns('SP500')

# Add a column for the Nasdaq
df['NDX'] = get_returns('NDX')

# Calculate correlations, plot the last 200 data points.
# Correlation window = last 200 days
plt = df['SP500'].rolling(50).corr(df['NDX'])[-200:].plot()
fig = plt.get_figure()
fig.savefig("output.png")

#df.plot()

#print(df)

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

for ind in data:
    data[ind + '_rebased'] = (data[-points_to_plot:][ind].pct_change() + 1).cumprod()
    
#data['SP500_rebased'].plot()

#data['NDX_rebased'].plot()