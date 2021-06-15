"""
计算所有基金的变动率，找出最高的三支基金。
计算动量最高的三支基金。
计算反转策略最好的三支基金，分别买入。

ATR AverageTrueRange

将所有基金的数据循环加载，只计算出最近10个交易日的 ATR 的平均值。

或者利用 pandas 进行计算，取出每天数据中的最大值和最小值，计算其差值百分比。
或者找出五个交易日中的最高价和最低差，计算差值百分比。
"""

import os

import pandas as pd

from backtest.backtest_get import all_etf_name_list


def cal_high_low(df):
    max = df['high'].max()
    min = df['low'].min()
    change = round((max - min) / min, 2)
    return change


def atr_max_10():
    datas = []
    fund_name_list = all_etf_name_list()

    mainpath = os.path.dirname(os.path.dirname(__file__))
    error_file_list = []
    changaes = dict()
    for fund in fund_name_list:
        try:
            path = os.path.join(mainpath, f'datas/{fund}.csv')
            data = pd.read_csv(path, encoding='utf-8')
            changaes[fund] = cal_high_low(data.tail(5))

        except FileNotFoundError:
            error_file_list.append(fund)

    changaes_df = pd.DataFrame.from_dict(changaes,
                                         orient='index',
                                         columns=['change'])

    changaes_df.sort_values(by='change', inplace=True, ascending=False)
    # print(changaes_df.head(10))
    change_list = changaes_df.head(10).to_dict()

    return change_list['change'].keys()


if __name__ == '__main__':
    print(atr_max_10())
