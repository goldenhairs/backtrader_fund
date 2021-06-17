import datetime

from backtest.backtest_cerebro import backtestopt, backtestrun
from backtest.backtest_strategy import (BBandStrategy, MomOscStrategy,
                                        MomStrategy)


def setup_data():
    """
    sz159915 创业板
    sz159949 创业板 50

    sh510310 沪深300
    sh510500 500etf
    
    sh518880 黄金ETF
    sh513100 纳指ETF
    
    测试三组数据
    1. 创业板 + 沪深300 + 中证500
    2. 创业板 50 + 沪深300 + 中证500
   
    3. 创业板 + 黄金 ETF + 纳指 ETF
    4. 创业板 50 + 黄金 ETF + 纳指 ETF
    
    group, period, Total ROI, Annual ROI 
    1, 16, 164.54%, 12.93%
    2, 16, 157.14%, 12.53%
    3, 18, 203.81%, 14.9%
    4, 18, 179.22%, 13.7%
    """
    hs300zz500 = ['sh510310', 'sh510500']

    funds_1 = ['sz159915'] + hs300zz500
    funds_2 = ['sz159952'] + hs300zz500

    gold_nas = ['sh518880', 'sh513100']

    funds_3 = ['sz159915'] + gold_nas
    funds_4 = ['sz159952'] + gold_nas

    res = {
        'funds_1': funds_1,
        'funds_2': funds_2,
        'funds_3': funds_3,
        'funds_4': funds_4
    }

    return res


def test_momoscstrategy(optflag=False, fund_name='funds_1'):
    datas = setup_data()
    cash = 200000.00
    periods = range(1, 60)

    opt_start_date = datetime.datetime(2017, 5, 28)

    run_start_date = datetime.datetime(2020, 1, 6)
    end_date = datetime.datetime.now()

    if optflag:
        backtestopt(cash=cash,
                    funds=datas[fund_name],
                    periods=periods,
                    start_date=opt_start_date,
                    end_date=end_date,
                    strategy=MomOscStrategy)
    else:
        backtestrun(cash=cash,
                    funds=datas[fund_name],
                    period=18,
                    start_date=run_start_date,
                    end_date=end_date,
                    strategy=MomOscStrategy)


def test_momstrategy(optflag=False, funds_name='funds_1'):
    datas = setup_data()
    cash = 200000.00
    periods = range(1, 60)

    opt_start_date = datetime.datetime(2017, 5, 28)
    opt_end_date = datetime.datetime.now()

    run_start_date = datetime.datetime(2020, 1, 6)
    run_end_date = datetime.datetime.now()

    if optflag:
        backtestopt(cash=cash,
                    funds=datas[funds_name],
                    periods=periods,
                    start_date=opt_start_date,
                    end_date=opt_end_date,
                    strategy=MomStrategy)
    else:
        backtestrun(cash=cash,
                    funds=datas[funds_name],
                    period=18,
                    start_date=run_start_date,
                    end_date=run_end_date,
                    strategy=MomStrategy)


def test_bbandstrategy(optflag=False, fund_name='funds_1'):
    datas = setup_data()
    cash = 200000.00
    periods = range(1, 60)

    opt_start_date = datetime.datetime(2017, 5, 28)
    run_start_date = datetime.datetime(2020, 1, 6)
    end_date = datetime.datetime.now()

    if optflag:
        backtestopt(cash=cash,
                    funds=datas[fund_name],
                    periods=periods,
                    start_date=opt_start_date,
                    end_date=end_date,
                    strategy=BBandStrategy)
    else:
        backtestrun(cash=cash,
                    funds=datas[fund_name],
                    period=18,
                    start_date=run_start_date,
                    end_date=end_date,
                    strategy=BBandStrategy)


if __name__ == '__main__':
    """
    1,16, 163.01%, 12.85%
    2,16, 156.6%, 12.5%
    3,18, 202.09%, 14.82%
    4,18, 178.64%, 13.67%
    """
    test_momoscstrategy(fund_name='funds_1', optflag=True)
    # test_momstrategy(funds_name='funds_1', optflag=True)
