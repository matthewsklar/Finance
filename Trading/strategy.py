# Dual Moving Average Trading Strategy

import pandas as pd
import pandas_datareader as pdr
import numpy as np
import matplotlib.pyplot as plt

import datetime

start = datetime.datetime(2006, 10, 1)
end = datetime.datetime(2016, 1, 1)
short_window = 40
long_window = 100

aapl = pdr.get_data_google('AAPL', start=start, end=end)
signals = pd.DataFrame(index=aapl.index)
fig = plt.figure()


def create_signals():
    signals['signal'] = 0.0
    signals['short_avg'] = aapl['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
    signals['long_avg'] = aapl['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

    signals['signal'][short_window:] = np.where(
        signals['short_avg'][short_window:] > signals['long_avg'][short_window:], 1.0, 0.0)

    signals['position'] = signals['signal'].diff()
    print(signals)


def graph():
    ax1 = fig.add_subplot(111, ylabel='Price in $')

    aapl['Close'].plot(ax=ax1, color='r', lw=2.)

    signals[['short_avg', 'long_avg']].plot(ax=ax1, lw=2.)

    ax1.plot(signals.loc[signals.position == 1.0].index, signals.short_avg[signals.position == 1.0],
             '^', markersize=10, color='m')
    ax1.plot(signals.loc[signals.position == -1.0].index, signals.short_avg[signals.position == -1.0],
             'v', markersize=10, color='k')

    plt.show()
