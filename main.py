import backtrader as bt

class TestStrategy(bt.Strategy):
    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=10)
        self.rsi = bt.indicators.RSI(self.data.close)

    def next(self):
        if self.rsi < 30 and self.data.close < self.sma:
            self.buy()
        elif self.rsi > 70 and self.data.close > self.sma:
            self.sell()

# Configuração do backtest
cerebro = bt.Cerebro()
data = bt.feeds.PandasData(dataname=df)
cerebro.adddata(data)
cerebro.addstrategy(TestStrategy)
cerebro.run()
