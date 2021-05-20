import calendar
import datetime

import backtrader as bt

import backtrader.analyzers as btanalyzers

def weekday(date):
    date_time = date
    return (calendar.weekday(date_time.year, date_time.month, date_time.day))


class strategy(bt.Strategy):
    params = (('maperiod', 20), )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataprice = self.datas[0].close
        self.rate = self.datas[0].volume
        self.all_size = 0
        self.all_fund_menoy = 0

    def next(self):
        if self.rate[0] <= -2.0 or self.rate[0] + self.rate[-1] <= -2.0:
            buysize = round(1000 / self.dataprice[0], 2)
            self.buy(size=buysize)


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    start_date = datetime.datetime(2019, 5, 14)
    # end_date = datetime.datetime(2020, 1, 7)
    end_date = datetime.datetime(2021, 5,20)

    data = bt.feeds.GenericCSVData(dataname='161017.csv',
                                   fromdate=start_date,
                                   todate=end_date,
                                   nullvalue=0.0,
                                   dtformat=('%Y-%m-%d'),
                                   datetime=0,
                                   open=-1,
                                   high=-1,
                                   low=-1,
                                   close=1,
                                   volume=2,
                                   openinterest=-1)

    cerebro.adddata(data)
    cerebro.addstrategy(strategy)

    cash = 100000
    cerebro.broker.setcash(cash)
    cerebro.broker.setcommission(commission=0.00015)

    cerebro.addanalyzer(btanalyzers.SharpeRatio_A, _name='sharp_a')
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='sharp')
    cerebro.addanalyzer(btanalyzers.AnnualReturn, _name='annualreturn')
    # cerebro.addanalyzer(btanalyzers.DrawDown, _name='drawdown')
    strats = cerebro.run()

    strat = strats[0]
    print(cerebro.broker.get_value())
    print(cerebro.broker.get_cash())
    print('夏普率:', strat.analyzers.sharp.get_analysis())
    print('夏普率a:', strat.analyzers.sharp_a.get_analysis())
    print('年化回报:', strat.analyzers.annualreturn.get_analysis())
    # print('最大回撤:', strat.analyzers.drawdown.get_analysis())
    cerebro.plot(volume=False)
