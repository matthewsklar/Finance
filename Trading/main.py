from Trading import backtest, strategy

import pandas_datareader as pdr
import datetime

if __name__ == '__main__':
    symbol = 'AAPL'
    start = datetime.datetime(2006, 10, 1)
    end = datetime.datetime(2016, 1, 1)
    bars = pdr.get_data_google(symbol, start=start, end=end)

    mac = strategy.MovingAverageCrossStrategy(bars, 40, 100)
    signals = mac.generate_signals()

    portfolio = backtest.MarketOnClosePortfolio(symbol, bars, signals, 100000.0)
    returns = portfolio.backtest_portfolio()

    mac.graph()
    portfolio.graph()
