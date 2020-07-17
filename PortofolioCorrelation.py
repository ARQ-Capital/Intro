%matplotlib inline
import pandas as pd
from matplotlib import pyplot as plt

PATH_HIST = 'C:\\Users\\acflo\\TradingEvolved\\hist\\'
ROLLING_DAY_WINDOW = 30

benchmarks = [ 'DIA', 'GLD', 'IWM', 'IYT',
               'SPY', 'TLT', 'XLC', 'XLF',
               'XLI', 'XLK', 'XLP', 'XLU' ]

stocks = []
w_file = 'watchlist.csv'
watchlist_file = pd.read_csv(w_file)
watchlist_file_len = int(watchlist_file.count())
for i in range(0, watchlist_file_len):
    a = watchlist_file.iloc[i,0]
    stocks.append(a)
    stocks_size = len(stocks)

def get_returns(file):
    """
    This function get_data reads a data file from disk.
    """
    return pd.read_csv(PATH_HIST + str(file) + "_price_history_" + '.csv', index_col=0, parse_dates=True).pct_change()
     
def calc_corr(ser1, ser2, window):
    """
    Calculates correlation between two series.
    """
    ret1 = ser1.pct_change()
    ret2 = ser2.pct_change()
    corr = ret1.rolling(window).corr(ret2)
    return corr

maxi = -2
max2 = -2
maxB = benchmarks[0]
maxB = benchmarks[0]

for elemS in stocks:
    df = get_returns(elemS)
    
    print('STOCK: ' + elemS)
    
    for elemB in benchmarks:
        df2 = get_returns(elemB)
        
        #print('BENCHMARK: ' + elemB)
        
        corrCoeff = df['4. close'].rolling(ROLLING_DAY_WINDOW).corr(df2['4. close'])[-300:]
        #print(corrCoeff[-1])
        
        if maxi < corrCoeff[-1]:
            max2 = maxi
            maxi = corrCoeff[-1]
            max2B = maxB
            maxB = elemB
        elif max2 < corrCoeff[-1]:
            max2 = corrCoeff[-1]
            max2B = elemB
            
    print('1ST CORR: ' + str(maxB))
    print('CORR COEFF: ' + str(maxi))
    
    print('2ND CORR: ' + str(max2B))
    print('CORR COEFF: ' + str(max2))
    
    print('\n\n\n')
