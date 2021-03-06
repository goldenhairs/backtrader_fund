import datetime

from backtest.backtest_cerebro import backtestopt, backtestrun
from backtest.backtest_strategy import (BBandMomoscStrategy, BBandStrategy,
                                        MomOscStrategy, MomStrategy)


def setup_data():
    """
    sz159915 创业板
    sz159949 创业板 50

    sh510310 沪深300
    sh510500 500etf
    
    sh518880 黄金ETF
    sh513100 纳指ETF
    


    sz159992 创新药
    sh512690 酒ETF
    
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

    jiuyao = ['sz159992', 'sh512690']
    funds_5 = ['sz159915'] + jiuyao

    res = {
        'funds_1': funds_1,
        'funds_2': funds_2,
        'funds_3': funds_3,
        'funds_4': funds_4,
        'funds_5': funds_5,
    }

    return res


def test_momoscstrategy(optflag=False, fund_name='funds_1', period=18):
    datas = setup_data()
    cash = 200000.00
    periods = range(1, 60)

    opt_start_date = datetime.datetime(2020, 4, 10)

    run_start_date = datetime.datetime(2021, 3, 1)
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
                    period=period,
                    start_date=opt_start_date,
                    end_date=end_date,
                    strategy=MomOscStrategy)


def test_momstrategy(optflag=False, funds_name='funds_1', period=18):
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
                    period=period,
                    start_date=opt_start_date,
                    end_date=run_end_date,
                    strategy=MomStrategy)


def test_bbandstrategy(optflag=False, fund_name='funds_1', period=18):
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
                    period=period,
                    start_date=run_start_date,
                    end_date=end_date,
                    strategy=BBandStrategy)


def test_oscbbandstrategy(optflag=False, fund_name='funds_1', period=18):
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
                    strategy=BBandMomoscStrategy)
    else:
        backtestrun(cash=cash,
                    funds=datas[fund_name],
                    period=period,
                    start_date=run_start_date,
                    end_date=end_date,
                    strategy=BBandMomoscStrategy)


if __name__ == '__main__':
    """
    momosc
    1, 19, 82.59%, 7.82%
    5, 14, 112.46%, 9.88%
    mom
    1, 3, 73.74%, 7.15%
    5, 13, 118.27%, 10.25%
    """
    # test_momoscstrategy(fund_name='funds_5', optflag=True)
    # test_momstrategy(funds_name='funds_1', optflag=True)

    test_momoscstrategy(fund_name='funds_5', period=14)
    # test_momstrategy(funds_name='funds_5', period=13)
