import datetime

import backtrader as bt
import backtrader.analyzers as btanalyzers
from backtrader import dataseries
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Tradimo


class BBandStrategy(bt.Strategy):
    """
    如果跌破布林下线则买入，跌破中线买入一半，从中线上涨到上线则卖出二分之一，从下线上涨到布林中线卖出二分之一。
    """

    params = (
        ('period', 20),
        ('printlog', True),
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataprice = self.datas[0].close
        self.order = None
        self.mid = bt.indicators.BollingerBands(self.datas[0],
                                                period=self.params.period).mid
        self.bot = bt.indicators.BollingerBands(self.datas[0],
                                                period=self.params.period).bot
        self.top = bt.indicators.BollingerBands(self.datas[0],
                                                period=self.params.period).top
        self.buy_value = []

    def next(self):

        position_size = self.broker.getposition(data=self.datas[0]).size
        self.log(f'{position_size}, {self.dataprice[0]}, {self.bot[0]}')

        if self.dataprice[0] <= self.bot[0] and position_size <= 0:
            self.order_target_percent(data=self.datas[0], target=0.3)
            self.buy_value.append(self.dataprice[0])

        if self.dataprice[0] <= self.bot[0] and position_size > 0:
            if self.dataprice[0] < self.buy_value[-1]:
                self.order_target_percent(data=self.datas[0], target=0.7)
                self.buy_value.append(self.dataprice[0])

        if self.dataprice[0] >= self.mid[0] and position_size > 0:
            self.order_target_percent(data=self.datas[0],
                                      target=position_size // 2)
            self.buy_value.append(self.dataprice[0])

        if self.dataprice[0] >= self.top[0] and position_size > 0:
            self.order_target_percent(data=self.datas[0], target=0)
            self.buy_value.clear()

        if self.dataprice[0] <= self.mid[0] and position_size <= 0:
            self.order_target_percent(data=self.datas[0], target=0.3)
            self.buy_value.append(self.dataprice[0])

    def stop(self):
        return_all = self.broker.getvalue() / 200000.0
        print('{0}, {1}%, {2}%'.format(
            self.params.period, round((return_all - 1.0) * 100, 2),
            round((pow(return_all, 1.0 / 8) - 1.0) * 100, 2)))


if __name__ == '__main__':
    """
    sz159915 创业板
    sz159992 创新药
    sh512690 酒ETF
    """

    import os
    import sys

    from backtest.backtest_feeds import ETFCsvData

    cash = 200000.00
    periods = range(1, 60)

    opt_start_date = datetime.datetime(2020, 4, 10)
    run_start_date = datetime.datetime(2020, 1, 6)
    end_date = datetime.datetime.now()

    cerebro = bt.Cerebro()
    # cerebro.optstrategy(BBandStrategy, period=periods, printlog=False)
    cerebro.addstrategy(BBandStrategy, period=18)

    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))

    datapath = os.path.join(modpath, f'datas/sz159915.csv')
    data = ETFCsvData(dataname=datapath,
                      fromdate=opt_start_date,
                      todate=end_date)
    cerebro.adddata(data)

    cerebro.broker.setcash(cash)
    cerebro.broker.setcommission(commission=0.00015)

    cerebro.addanalyzer(btanalyzers.SharpeRatio_A, _name='sharp')
    cerebro.addanalyzer(btanalyzers.AnnualReturn, _name='annualreturn')
    cerebro.addanalyzer(btanalyzers.Returns, _name='return')
    cerebro.addanalyzer(btanalyzers.SQN, _name='SQN')

    cerebro.run()
    b = Bokeh(style='bar', scheme=Tradimo())
    cerebro.plot(b)
