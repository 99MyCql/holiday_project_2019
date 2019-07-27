# -*- coding: utf-8 -*-
'''
对岗位薪资数据的分析
'''
import pandas as pd
import numpy as np

df = pd.read_csv('job2.csv', encoding='utf-8')
print(df.info())
print(df['职位'].unique())
print(df['职位'].nunique())
