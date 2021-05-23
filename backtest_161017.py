import datetime
from backtest.backtest_feeds import OpenFundCsvData, ETFCsvData
from backtest.backtest_strategy import DeclineStrategy

import backtrader as bt
import backtrader.analyzers as btanalyzers


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    start_date = datetime.datetime(2020, 7, 23)
    end_date = datetime.datetime(2021, 5, 20)

    data = OpenFundCsvData(dataname=r'datas/161017.csv',
                           fromdate=start_date,
                           todate=end_date,)

    data1 = ETFCsvData(dataname=r'datas/sh510500.csv', fromdate=start_date, todate=end_date)
    cerebro.adddata(data1)
    cerebro.addstrategy(DeclineStrategy)

    cash = 100000
    cerebro.broker.setcash(cash)
    cerebro.broker.setcommission(commission=0.00015)

    cerebro.addanalyzer(btanalyzers.SharpeRatio_A, _name='sharp')
    cerebro.addanalyzer(btanalyzers.AnnualReturn, _name='annualreturn')

    strats = cerebro.run()
    strat = strats[0]

    return_all = cerebro.broker.get_value() - cash
    used_cash = cash - cerebro.broker.get_cash()
    # roi = round(return_all/used_cash, 2) * 100
    print('夏普率:', strat.analyzers.sharp.get_analysis())
    print('年化回报:', strat.analyzers.annualreturn.get_analysis())
    # print(f'总收益: {roi}%')

    cerebro.plot()
