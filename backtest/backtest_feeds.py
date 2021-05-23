"""
编写私有的数据文件类。
"""
from backtrader.feeds import GenericCSVData


class ETFCsvData(GenericCSVData):
    params = (
        ('nullvalue', 0.0),
        ('dtformat', '%Y-%m-%d'),
        ('datetime', 1),
        ('open', 2),
        ('high', 3),
        ('low', 4),
        ('close', 5),
        ('volume', 6),
        ('openinterest', -1),
    )

class OpenFundCsvData(GenericCSVData):
    params = (
        ('nullvalue', 0.0),
        ('dtformat', '%Y-%m-%d'),
        ('datetime', 0),
        ('open', -1),
        ('high', -1),
        ('low', -1),
        ('close', 1),
        ('volume', 2),
        ('openinterest', -1),
    )
