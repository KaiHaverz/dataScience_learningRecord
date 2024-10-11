import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

file_data=pd.read_csv('./chengdu_rent.csv')
file_data.head()

# 重复数据检测
file_data.duplicated()