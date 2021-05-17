import calendar
import datetime

import backtrader as bt


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
        self.all_size = 0
        self.all_fund_menoy = 0

    def next(self):
        if weekday(self.datas[0].datetime.date(0)) == 3:
            buy_size = round(250 / self.dataprice[0], 2)
            self.all_fund_menoy += 250
            self.buy(size=buy_size)


if __name__ == '__main__':
    import backtrader.analyzers as btanalyzers
    cerebro = bt.Cerebro()
    start_date = datetime.datetime(2018, 1, 1)
    end_date = datetime.datetime(2021, 5, 13)

    data = bt.feeds.GenericCSVData(dataname='sh513050.csv',
                                   fromdate=start_date,
                                   todate=end_date,
                                   nullvalue=0.0,
                                   dtformat=('%Y-%m-%d'),
                                   datetime=1,
                                   open=2,
                                   high=3,
                                   low=4,
                                   close=5,
                                   volume=6,
                                   openinterest=-1)

    cerebro.adddata(data)
    cerebro.addstrategy(strategy)

    cash = 100000
    cerebro.broker.setcash(cash)
    cerebro.broker.setcommission(commission=0.00015)
    cerebro.addanalyzer(btanalyzers.SharpeRatio_A, _name='sharp')
    cerebro.addanalyzer(btanalyzers.AnnualReturn, _name='annualreturn')

    strats = cerebro.run()
    strat = strats[0]
    print('夏普率:', strat.analyzers.sharp.get_analysis())
    print('年化回报:', strat.analyzers.annualreturn.get_analysis())
