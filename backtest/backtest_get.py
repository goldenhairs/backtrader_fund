import akshare as ak
import os
import sys

mainpath = os.path.dirname(os.path.dirname(__file__))

def get_all_fund_list():
    """
    获取所有基金数据
    """
    fund_em_fund_name_df = ak.fund_em_fund_name()
    path = os.path.join(mainpath, f'datas/all_fund.csv')
    fund_em_fund_name_df.to_csv(path)


def get_etf_list():
    """
    获取etf基金清单
    """
    fund_list = ak.fund_etf_category_sina(symbol="ETF基金")
    path = os.path.join(mainpath, f'datas/etf_list.csv')
    fund_list.to_csv(path, encoding='utf-8')


def get_fund_detail(etf_fund_code):
    """
    获取 ETF 基金数据
    """
    fund_detail = ak.fund_etf_hist_sina(symbol=etf_fund_code)
    path = os.path.join(mainpath, f'datas/{etf_fund_code}.csv')
    fund_detail.to_csv(path, encoding='utf-8')


def get_open_fund_info(fund_code):
    """
    获取开放式基金数据
    """
    fund_data = ak.fund_em_open_fund_info(fund=fund_code, indicator="单位净值走势")
    fund_data_new = fund_data.rename(columns={
        '净值日期': 'datetime',
        '单位净值': 'open',
        '日增长率': 'rate',
    })
    result_data = fund_data_new[['datetime', 'open', 'rate']]
    path = os.path.join(mainpath, f'datas/{fund_code}.csv')
    result_data.to_csv(path, index=None, encoding='utf-8')


def download_open_fund():
    """
    广发多因子混合 002943
    广发价值领先混合 008099
    富国中证 500 指数 161017
    """
    fund_list = ['161017', '002943', '008099']
    for fund in fund_list:
        get_open_fund_info(fund_code=fund)


def download_etf_fund():
    """
    sh513050 中概互联
    sz159992 创新药

    sz159952 创业etf
    sh510500 500etf
    sz159949 创业板 50
    sh510310 沪深300

    sz159915 创业板
    sh518880 黄金ETF
    sh513100 纳指ETF
    """
    funds = ['sh513050', 'sz159992', 'sz159952', 'sh510500', 'sz159949', 'sh510310', 'sz159915', 'sh518880', 'sh513100']
    for fun in funds:
        get_fund_detail(fun)


if __name__ == '__main__':
    #get_all_fund_list()
    #get_etf_list()

    download_etf_fund()
    download_open_fund()