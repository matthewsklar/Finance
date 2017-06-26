from Trading import strategy as stgy
import matplotlib.pyplot as plt

initial_capital = 100000.0

def run():
    signals = stgy.signals
    aapl = stgy.aapl

    positions = stgy.pd.DataFrame(index=signals.index)
    positions['AAPL'] = 100*signals['signal']

    portfolio = positions.multiply(aapl['Close'], axis=0)

    pos_diff = positions.diff()

    portfolio['holdings'] = (positions.multiply(aapl['Close'], axis=0)).sum(axis=1)
    portfolio['cash'] = initial_capital - (pos_diff.multiply(aapl['Close'], axis=0)).sum(axis=1).cumsum()
    portfolio['total'] = portfolio['cash'] + portfolio['holdings']
    portfolio['returns'] = portfolio['total'].pct_change()

    print(portfolio)

    fig = plt.figure()
    ax1 = fig.add_subplot(111, ylabel='Portfolio value in $')

    portfolio['total'].plot(ax=ax1, lw=2.)

    ax1.plot(portfolio.loc[signals.position == 1.0].index,
             portfolio.total[signals.position == 1.0],
             '^', markersize=10, color='m')
    ax1.plot(portfolio.loc[signals.position == -1.0].index,
             portfolio.total[signals.position == -1.0],
             'v', markersize=10, color='k')

    plt.show()

def graph():
    pass

