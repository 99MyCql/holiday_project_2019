'''
数据管理模块
'''
import pandas as pd
import numpy as np

FILE_51JOB = 'data/jobs_51job.csv'

class DataAnalysis:
    def __init__(self):
        self.df = pd.read_csv(FILE_51JOB, encoding='utf-8')
        self.df.info()
        print(self.df.columns)
        self.keys = self.df['职位名称关键字'].unique()
        print(self.keys)
        print(self.df.groupby('职位名称关键字').count())

    # 获取关键字位 key 的岗位的信息
    def get_station_info(self, key):
        new_df = self.df[self.df['职位名称关键字'] == key] # 提取对应关键字岗位的数据
        count = new_df['职位名称'].count()
        mean_salary = new_df['职位薪资'].mean()
        city_list = list(new_df.groupby('地区')['职位名称'].count().index) # 获取城市名
        count_city_list = list(new_df.groupby('地区')['职位名称'].count().values) # 获取城市名对应的岗位数量
        city_dict = dict(zip(city_list, count_city_list)) # 转换成字典
        max_index = count_city_list.index(max(count_city_list)) # 获取岗位数量最多的城市下标
        return {
            'station_name': key, # 岗位关键字名
            'count': count, # 岗位数量
            'mean_salary': int(mean_salary), # 岗位平均薪资
            'max_count_city': city_list[max_index], # 岗位数量最多的城市
            'max_count': count_city_list[max_index], # 数量最多城市的岗位数量
            'city_dict': city_dict # {城市: 岗位数量} 的字典序
        }


data_analysis = DataAnalysis() # 单例模式

if __name__ == '__main__':
    print(data_analysis.get_station_info('人工智能'))