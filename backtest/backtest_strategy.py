import backtrader as bt
import calendar

"""
实现富国中证 500 定投，如果跌幅达到 2% 则买入
"""


class DeclineStrategy(bt.Strategy):
    params = (
        ('decline', -2.0),
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataprice = self.datas[0].close
        self.rate = (self.datas[0].close - self.datas[0].open) / self.datas[0].open * 100

    def next(self):
        print(self.rate[0])
        if self.rate[0] <= self.params.decline or (self.rate[0] + self.rate[-1]) <= self.params.decline:
            buy_size = round(250 / self.dataprice[0], 2)
            print(buy_size)
            self.buy(size=100)


"""
实现在每周的一天进行定投
"""


class WeekStrategy(bt.Strategy):
    params = (('weeknum', 3),)

    def weekday(self, date):
        date_time = date
        return (calendar.weekday(date_time.year, date_time.month, date_time.day))

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataprice = self.datas[0].close

    def next(self):
        if self.weekday(self.datas[0].datetime.date(0)) == self.params.weeknum:
            buy_size = round(250 / self.dataprice[0], 2)
            self.buy(size=buy_size)


"""
动量钟摆策略
"""


class MomOscStrategy(bt.Strategy):
    params = (
        ('period', 20),
    )

    def __init__(self):
        self.dataprice = self.datas[0].close
        self.order = None
        self.month = -1
        self.mom = [bt.indicators.MomentumOscillator(i, period=self.params.period) for i in self.datas]

    def next(self):
        buy_id = 0

        c = [i.momosc[0] for i in self.mom]
        index, value = c.index(max(c)), max(c)

        if value > 100:
            buy_id = index

        for i in range(0, len(c)):
            if i != buy_id:
                position_size = self.broker.getposition(data=self.datas[i]).size
                if position_size != 0:
                    self.order_target_percent(data=self.datas[i], target=0)

        position_size = self.broker.getposition(data=self.datas[buy_id]).size
        if position_size == 0:
            self.order_target_percent(data=self.datas[buy_id], target=0.98)

    def stop(self):
        return_all = self.broker.getvalue() / 200000.0
        print('{0}, {1}%, {2}%'.format(self.params.period,
                                       round((return_all - 1.0) * 100, 2),
                                       round((pow(return_all, 1.0 / 8) - 1.0) * 100, 2)
                                       ))


class MomStrategy(bt.Strategy):
    params = (
        ('period', 20),
    )

    def __init__(self):
        self.dataprice = self.datas[0].close
        self.order = None
        self.month = -1
        self.mom = [bt.indicators.Momentum(i, period=self.params.period) for i in self.datas]

    def next(self):
        buy_id = 0

        c = [i.momentum[0] for i in self.mom]
        index, value = c.index(max(c)), max(c)

        if value > 0:
            buy_id = index

        for i in range(0, len(c)):
            if i != buy_id:
                position_size = self.broker.getposition(data=self.datas[i]).size
                if position_size != 0:
                    self.order_target_percent(data=self.datas[i], target=0)

        position_size = self.broker.getposition(data=self.datas[buy_id]).size
        if position_size == 0:
            self.order_target_percent(data=self.datas[buy_id], target=0.98)

    def stop(self):
        return_all = self.broker.getvalue() / 200000.0
        print('{0}, {1}%, {2}%'.format(self.params.period,
                                       round((return_all - 1.0) * 100, 2),
                                       round((pow(return_all, 1.0 / 8) - 1.0) * 100, 2)
                                       ))


class BBandStrategy(bt.Strategy):
    params = (
        ('period', 20),
    )

    def __init__(self):
        self.dataprice = self.datas[0].close
        self.order = None
        self.month = -1
        self.bbandPcts = [bt.indicators.BollingerBandsPct(i, period=self.params.period) for i in self.datas]

    def next(self):
        buy_id = 0

        c = [i.pctb[0] for i in self.bbandPcts]
        index, value = c.index(max(c)), max(c)

        if value > 0:
            buy_id = index

        for i in range(0, len(c)):
            if i != buy_id:
                position_size = self.broker.getposition(data=self.datas[i]).size
                if position_size != 0:
                    self.order_target_percent(data=self.datas[i], target=0)

        position_size = self.broker.getposition(data=self.datas[buy_id]).size
        if position_size == 0:
            self.order_target_percent(data=self.datas[buy_id], target=0.98)

    def stop(self):
        return_all = self.broker.getvalue() / 200000.0
        print('{0}, {1}%, {2}%'.format(self.params.period,
                                       round((return_all - 1.0) * 100, 2),
                                       round((pow(return_all, 1.0 / 8) - 1.0) * 100, 2)
                                       ))
