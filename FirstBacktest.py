# Make sure the plot shows up
%matplotlib inline

# Import libraries that we need
import pandas as pd
import numpy as np

# Read the data from disk into a Pandas Dataframe (i.e. spreadsheet)
# Open csv file called sp500, take the column called Date and 
# parse the results from that column as being Dates (regardless of the date type)
data = pd.read_csv('sp500.csv', index_col='Date', parse_dates=['Date'])

#data /= 1000

# take the moving average for the last 50, respectively 200 values
data['SMA50'] = data['SP500'].rolling(50).mean()
data['SMA200'] = data['SP500'].rolling(200).mean()

# take the moving average of 50, respectively 200 values and store on the Position column
# the moments when we should sale (SMA50 > SMA200, so we have value 1), or buy (in the opposite case)
data['Position'] = np.where(data['SMA50'] > data['SMA200'], 1, 0)

# Buy a day delayed, shift the column
data['Position'] = data['Position'].shift()

# Calculate the daily percent returns of strategy
data['StrategyPct'] = data['SP500'].pct_change(1) * data['Position']

# this tells us (in percentage) how much we are expected to win if we follow this strategy 
# (ex. we start with 100.000$ in 2010 and, according to the dataset, are expected to reach 150.000$ by 2019)
data['StrategyPct'] = (data['StrategyPct'] + 1).cumprod()

# calculate index cumulative returns
# when we buy something and keep it without having any interest
# in what happens to that thing in the future
data['BuyHold'] = (data['SP500'].pct_change(1) + 1).cumprod()

# plot the values of the data spreadsheet 
data[['SP500', 'BuyHold']].plot(figsize=(20,10))