from Trading import backtest

if __name__ == '__main__':
    backtest.stgy.create_signals()
    backtest.stgy.graph()
    backtest.run()
