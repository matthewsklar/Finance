# Dual Moving Average Trading Strategy
from abc import ABCMeta, abstractmethod

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Strategy(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def generate_signals(self):
        raise NotImplementedError("Implement generate_signals()")

    @abstractmethod
    def graph(self):
        raise NotImplementedError("Implement graph()")


class MovingAverageCrossStrategy(Strategy):
    def __init__(self, bars, short_window, long_window):
        self.bars = bars
        self.short_window = short_window
        self.long_window = long_window
        self.signals = None

    def generate_signals(self):
        signals = pd.DataFrame(index=self.bars.index)
        signals['signal'] = 0.0

        signals['short_avg'] = self.bars['Close'].rolling(window=self.short_window, min_periods=1, center=False).mean()
        signals['long_avg'] = self.bars['Close'].rolling(window=self.long_window, min_periods=1, center=False).mean()

        signals['signal'][self.short_window:] = np.where(
            signals['short_avg'][self.short_window:] > signals['long_avg'][self.short_window:], 1.0, 0.0)

        signals['position'] = signals['signal'].diff()

        self.signals = signals
        return signals

    def graph(self):
        ax1 = plt.figure().add_subplot(111, ylabel='Price in $')

        self.bars['Close'].plot(ax=ax1, color='r', lw=2.)

        self.signals[['short_avg', 'long_avg']].plot(ax=ax1, lw=2.)

        ax1.plot(self.signals.loc[self.signals.position == 1.0].index,
                 self.signals.short_avg[self.signals.position == 1.0], '^', markersize=10, color='m')
        ax1.plot(self.signals.loc[self.signals.position == -1.0].index, 
                 self.signals.short_avg[self.signals.position == -1.0], 'v', markersize=10, color='k')

        plt.show()
