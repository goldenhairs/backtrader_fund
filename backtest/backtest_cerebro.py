import os
import sys

import backtrader as bt
import backtrader.analyzers as btanalyzers
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Tradimo

from backtest.backtest_feeds import ETFCsvData


def backtestopt(cash, funds, periods, start_date, end_date, strategy):

    cerebro = bt.Cerebro()
    cerebro.optstrategy(strategy, period=periods, printlog=False)

    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))

    for fund in funds:
        datapath = os.path.join(modpath, f'datas/{fund}.csv')
        data = ETFCsvData(dataname=datapath,
                          fromdate=start_date,
                          todate=end_date)
        cerebro.adddata(data)

    cerebro.broker.setcash(cash)
    cerebro.broker.setcommission(commission=0.00015)

    print('period, Total ROI, Annual ROI')

    cerebro.run()


def backtestrun(cash, funds, period, start_date, end_date, strategy):

    cerebro = bt.Cerebro()
    cerebro.addstrategy(strategy, period=period)

    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))

    for fund in funds:
        datapath = os.path.join(modpath, f'datas/{fund}.csv')
        data = ETFCsvData(dataname=datapath,
                          fromdate=start_date,
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
