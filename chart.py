import os

import matplotlib.pyplot as plt
import pandas as pd
from pandas.core.frame import DataFrame

mainpath = os.path.dirname(os.path.dirname(__file__))

csv = os.path.join(mainpath, f'views/ss.csv')
data = pd.read_csv(
    csv,
    encoding='utf-8',
)
datas_1 = pd.pivot_table(data, index=['日期'], columns=['基金代码'], values=['动量值'])

print(datas_1.head())

datas_1.plot()
plt.show()
