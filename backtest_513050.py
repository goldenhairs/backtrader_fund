import datetime

import backtrader as bt
from backtest.backtest_feeds import ETFCsvData
from backtest.backtest_strategy import WeekStrategy

import backtrader.analyzers as btanalyzers

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    start_date = datetime.datetime(2018, 1, 1)
    end_date = datetime.datetime(2021, 5, 13)

    data = ETFCsvData(dataname=r'datas/sh513050.csv',
                      fromdate=start_date,
                      todate=end_date,)

    cerebro.adddata(data)
    cerebro.addstrategy(WeekStrategy)

    cash = 100000
    cerebro.broker.setcash(cash)
    cerebro.broker.setcommission(commission=0.00015)

    cerebro.addanalyzer(btanalyzers.SharpeRatio_A, _name='sharp')
    cerebro.addanalyzer(btanalyzers.AnnualReturn, _name='annualreturn')

    strats = cerebro.run()
    strat = strats[0]

    return_all = cerebro.broker.get_value() - cash
    used_cash = cash - cerebro.broker.get_cash()
    roi = round(return_all/used_cash, 2) * 100
    print('夏普率:', strat.analyzers.sharp.get_analysis())
    print('年化回报:', strat.analyzers.annualreturn.get_analysis())
    print(f'总收益: {roi}%')

    cerebro.plot()
