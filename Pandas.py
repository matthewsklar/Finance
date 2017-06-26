import pandas_datareader as pdr
import matplotlib.pyplot as plt

import datetime

aapl = pdr.get_data_google('AAPL', start=datetime.datetime(2010, 10, 1), end=datetime.datetime(2016, 1, 1))

# aapl.to_csv('aapl_ohlc.csv')
# df = pd.read_csv('aapl_ohlc.csv', header=0, index_col='Date', parse_dates=True)

sample = aapl.sample()

print(aapl.pct_change().describe())

aapl.resample('BM').mean().pct_change().cumprod().plot(grid=True)

plt.show()
