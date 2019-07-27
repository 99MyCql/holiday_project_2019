'''
数据管理模块
'''
from pandas as pd
from numpy as np

FILE_51JOB = 'jobs_51job.csv'

class DataAnalysis:
    def __init__(self):
        self.df = pd.read_csv(FILE_51JOB)

    def get_station_list(self):
        self.df