import calendar

import backtrader as bt


class MyStrategy(bt.Strategy):
    params = (('printlog', False), )

    def log(self, txt, dt=None, doprint=False):
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        pass

    def next(self):
        pass

    def stop(self):
        pass

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f'执行买入，{order.data._name}，价格：{order.executed.price:.2f}，花费：{order.executed.value:.2f}，手续费：{order.executed.comm:.2f}'
                )

            else:
                self.log(
                    f'执行卖出，{order.data._name}，价格：{order.executed.price:.2f}，花费：{order.executed.value:.2f}，手续费：{order.executed.comm:.2f}'
                )
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('交易取消、保证金不足、交易被拒绝')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log(f'营业利润，毛利润：{trade.pnl:.2f}，净利润：{trade.pnlcomm:.2f}')


"""
实现富国中证 500 定投，如果跌幅达到 2% 则买入
"""


class DeclineStrategy(bt.Strategy):
    params = (('decline', -2.0), )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataprice = self.datas[0].close
        self.rate = (self.datas[0].close -
                     self.datas[0].open) / self.datas[0].open * 100

    def next(self):
        print(self.rate[0])
        if self.rate[0] <= self.params.decline or (
                self.rate[0] + self.rate[-1]) <= self.params.decline:
            buy_size = round(250 / self.dataprice[0], 2)
            print(buy_size)
            self.buy(size=100)


"""
实现在每周的一天进行定投
"""


class WeekStrategy(bt.Strategy):
    params = (('weeknum', 3), )

    def weekday(self, date):
        date_time = date
        return (calendar.weekday(date_time.year, date_time.month,
                                 date_time.day))

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


class MomOscStrategy(MyStrategy):
    params = (
        ('period', 20),
        ('printlog', True),
    )

    def __init__(self):
        self.dataprice = self.datas[0].close
        self.order = None
        self.month = -1
        self.mom = [
            bt.indicators.MomentumOscillator(i, period=self.params.period)
            for i in self.datas
        ]

    def next(self):
        buy_id = 999

        c = [i.momosc[0] for i in self.mom]
        [self.log(f'{self.datas[c.index(i)]._name}, {i}') for i in c]
        index, value = c.index(max(c)), max(c)

        if value > 100:
            buy_id = index

        for i in range(0, len(c)):

            if i != buy_id:
                position_size = self.broker.getposition(
                    data=self.datas[i]).size
                if position_size != 0:
                    self.order_target_percent(data=self.datas[i], target=0)

        if buy_id != 999:
            position_size = self.broker.getposition(
                data=self.datas[buy_id]).size
            if position_size == 0:
                self.order_target_percent(data=self.datas[buy_id], target=0.98)

    def stop(self):
        return_all = self.broker.getvalue() / 200000.0
        print('{0}, {1}%, {2}%'.format(
            self.params.period, round((return_all - 1.0) * 100, 2),
            round((pow(return_all, 1.0 / 8) - 1.0) * 100, 2)))


class MomStrategy(MyStrategy):
    params = (
        ('period', 20),
        ('printlog', True),
    )

    def __init__(self):
        self.dataprice = self.datas[0].close
        self.order = None
        self.month = -1
        self.mom = [
            bt.indicators.Momentum(i, period=self.params.period)
            for i in self.datas
        ]

    def next(self):
        buy_id = 999

        c = [
            i.momentum[0]  #/ (i.datas[0].close + i.datas[0].open) * 2
            for i in self.mom
        ]
        index, value = c.index(max(c)), max(c)
        [self.log(f'{self.datas[c.index(i)]._name}, {i}') for i in c]
        if value > 0:
            buy_id = index

        for i in range(0, len(c)):
            if i != buy_id:
                position_size = self.broker.getposition(
                    data=self.datas[i]).size
                if position_size != 0:
                    self.order_target_percent(data=self.datas[i], target=0)

        if buy_id != 999:
            position_size = self.broker.getposition(
                data=self.datas[buy_id]).size
            if position_size == 0:
                self.order_target_percent(data=self.datas[buy_id], target=0.98)

    def stop(self):
        return_all = self.broker.getvalue() / 200000.0
        print('{0}, {1}%, {2}%'.format(
            self.params.period, round((return_all - 1.0) * 100, 2),
            round((pow(return_all, 1.0 / 8) - 1.0) * 100, 2)))


class BBandStrategy(bt.Strategy):
    params = (('period', 20), )

    def __init__(self):
        self.dataprice = self.datas[0].close
        self.order = None
        self.month = -1
        self.bbandPcts = [
            bt.indicators.BollingerBandsPct(i, period=self.params.period)
            for i in self.datas
        ]

    def next(self):
        buy_id = 0

        c = [i.pctb[0] for i in self.bbandPcts]
        index, value = c.index(max(c)), max(c)

        if value > 0:
            buy_id = index

        for i in range(0, len(c)):
            if i != buy_id:
                position_size = self.broker.getposition(
                    data=self.datas[i]).size
                if position_size != 0:
                    self.order_target_percent(data=self.datas[i], target=0)

        position_size = self.broker.getposition(data=self.datas[buy_id]).size
        if position_size == 0:
            self.order_target_percent(data=self.datas[buy_id], target=0.98)

    def stop(self):
        return_all = self.broker.getvalue() / 200000.0
        print('{0}, {1}%, {2}%'.format(
            self.params.period, round((return_all - 1.0) * 100, 2),
            round((pow(return_all, 1.0 / 8) - 1.0) * 100, 2)))


class bband_momosc(MyStrategy):
    """
    先找到动量最好的一支，然后判断，如果跌破布林下线则买入，跌破中线买入一半，从中线上涨到上线则卖出二分之一，从下线上涨到布林中线卖出二分之一。
    """
    pass
    
