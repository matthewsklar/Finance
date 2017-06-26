from abc import ABCMeta, abstractmethod

from Trading import strategy as stgy
import matplotlib.pyplot as plt

initial_capital = 100000.0

class Portfolio(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def generate_positions(self):
        raise NotImplementedError("Implement generate_positions()")

    @abstractmethod
    def backtest_portfolio(self):
        raise NotImplementedError("Implement backtest_portfolio()")

    @abstractmethod
    def graph(self):
        raise NotImplementedError("Implement graph()")

class MarketOnClosePortfolio(Portfolio):
    def __init__(self, symbol, bars, signals, initial_capital):
        self.symbol = symbol
        self.bars = bars
        self.signals = signals
        self.initial_capital = float(initial_capital)
        self.positions = self.generate_positions()

    def generate_positions(self):
        positions = stgy.pd.DataFrame(index=self.signals.index)
        positions[self.symbol] = 100*self.signals['signal']

        return positions

    def backtest_portfolio(self):
        portfolio = self.positions.multiply(self.bars['Close'], axis=0)
        pos_diff = self.positions.diff()

        portfolio['holdings'] = (self.positions.multiply(self.bars['Close'], axis=0)).sum(axis=1)
        portfolio['cash'] = initial_capital - (pos_diff.multiply(self.bars['Close'], axis=0)).sum(axis=1).cumsum()
        portfolio['total'] = portfolio['cash'] + portfolio['holdings']
        portfolio['returns'] = portfolio['total'].pct_change()

        self.portfolio = portfolio
        return portfolio

    def graph(self):
        fig = plt.figure()
        ax1 = fig.add_subplot(111, ylabel='Portfolio value in $')

        self.portfolio['total'].plot(ax=ax1, lw=2.)

        ax1.plot(self.portfolio.loc[self.signals.position == 1.0].index,
                 self.portfolio.total[self.signals.position == 1.0],
                 '^', markersize=10, color='m')
        ax1.plot(self.portfolio.loc[self.signals.position == -1.0].index,
                 self.portfolio.total[self.signals.position == -1.0],
                 'v', markersize=10, color='k')

        plt.show()
