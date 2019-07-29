'''
数据管理模块
'''
import pandas as pd
import numpy as np

FILE_ALL = 'data/jobs.csv'
FILE_51JOB = 'data/jobs_51job.csv'
FILE_LAGOU = 'data/jobs_lagou.csv'
FILE_BOSS = 'data/jobs_boss.csv'
FILE_HOUSE_PRICE = 'data/house_price.csv'

STATION_SKIL_FOLDER = 'data/station_skill/'

class DataAnalysis:
    def __init__(self):
        self.df_house_price = pd.read_csv(FILE_HOUSE_PRICE, encoding='utf-8') # 各城市房价信息
        self.df_house_price.info()

        self.df = pd.read_csv(FILE_ALL, encoding='utf-8')
        self.df.info()
        print(self.df.columns)

        self.keys = self.df['职位名称关键字'].unique() # 岗位关键字
        print(self.keys)
        # print(self.df.groupby('职位名称关键字').count())

    # 获取房价信息列表
    def get_house_price_citys(self):
        ret_list = []
        for item in self.df_house_price.values:
            ret_list.append({
                'name': item[0],
                'value': int(item[1])
            })
        return ret_list

    # 获取对应城市房价
    def get_house_price(self, city):
        temp = self.df_house_price[self.df_house_price['city'] == city]
        return temp['house_price'].values[0]

    # 获取关键字位 key 的岗位的信息
    def get_station_info(self, key):
        new_df = self.df[self.df['职位名称关键字'] == key] # 提取对应关键字岗位的数据
        count = new_df['职位名称'].count()
        mean_salary = new_df['职位薪资'].mean()
        city_list = list(new_df.groupby('地区')['职位名称'].count().index) # 获取城市名
        count_city_list = list(new_df.groupby('地区')['职位名称'].count().values) # 获取城市名对应的岗位数量
        max_index = count_city_list.index(max(count_city_list)) # 获取岗位数量最多的城市下标
        return {
            'station_name': key, # 岗位关键字名
            'count': count, # 岗位数量
            'mean_salary': int(mean_salary), # 岗位平均薪资
            'max_count_city': city_list[max_index], # 岗位数量最多的城市
            'max_count': count_city_list[max_index] # 数量最多城市的岗位数量
        }

    # 获取对应岗位需具备的技能和占比
    def get_station_skill(self, key):
        if key == '运维/技术支持':
            key = '运维'
        if key == '电子/半导体':
            key = '电子'
        with open(STATION_SKIL_FOLDER + key + '.txt', 'r', encoding='utf-8') as f:
            data = f.read().split()[2:]
            print(data)
            kill_dict = {}
            ret = []
            for i in data:
                temp = i.split(',')
                ret.append({
                    'name': temp[0],
                    'value': float(temp[1])
                })
            return ret

    # 获取岗位在每个城市的信息
    def get_station_info_citys(self, key):
        new_df = self.df[self.df['职位名称关键字'] == key] # 提取对应关键字岗位的数据
        city_list = list(new_df.groupby('地区')['职位名称'].count().index) # 获取城市名
        count_city_list = list(new_df.groupby('地区')['职位名称'].count().values) # 获取每个城市对应的岗位数量
        salary_city_list = list(new_df.groupby('地区')['职位薪资'].mean().values) # 获取每个城市对应的薪资平均值
        return {
            'city_list': city_list,
            'count_city_list': count_city_list,
            'salary_city_list': salary_city_list
        }

    # 返回拉勾网站数据的各岗位信息
    def get_lagou_stations_info(self):
        df_lagou = pd.read_csv(FILE_LAGOU, encoding='utf-8') # 拉钩网站信息
        list_lagou_stations_info = []
        for key in self.keys:
            df_temp = df_lagou[df_lagou['职位名称关键字'] == key]
            # 为NaN
            mean = df_temp['职位薪资'].mean()
            if mean != mean:
                mean = 0
            list_lagou_stations_info.append({
                'count': df_temp['职位名称'].count(), # 岗位数量
                'mean_salary': int(mean) # 岗位平均薪资
            })
        return list_lagou_stations_info

    # 返回boss网站数据的各岗位信息
    def get_boss_stations_info(self):
        df_boss = pd.read_csv(FILE_BOSS, encoding='utf-8') # 拉钩网站信息
        list_boss_stations_info = []
        for key in self.keys:
            df_temp = df_boss[df_boss['职位名称关键字'] == key]
            # 为NaN
            mean = df_temp['职位薪资'].mean()
            if mean != mean:
                mean = 0
            list_boss_stations_info.append({
                'count': df_temp['职位名称'].count(), # 岗位数量
                'mean_salary': int(mean) # 岗位平均薪资
            })
        return list_boss_stations_info

    # 返回51job网站数据的各岗位信息
    def get_51job_stations_info(self):
        df_51job = pd.read_csv(FILE_51JOB, encoding='utf-8') # 51job网站信息
        list_51job_stations_info = []
        for key in self.keys:
            df_temp = df_51job[df_51job['职位名称关键字'] == key]
            # 为NaN
            mean = df_temp['职位薪资'].mean()
            if mean != mean:
                mean = 0
            list_51job_stations_info.append({
                'count': df_temp['职位名称'].count(), # 岗位数量
                'mean_salary': int(mean) # 岗位平均薪资
            })
        return list_51job_stations_info

    # 对应岗位不同学历的最大薪资、最小薪资、平均薪资
    def get_salary_degree(self, key):
        new_df = self.df[self.df['职位名称关键字'] == key] # 提取对应关键字岗位的数据
        # print(new_df.groupby('学历要求')['职位薪资'].max())
        # print(new_df.groupby('学历要求')['职位薪资'].min())
        # print(new_df.groupby('学历要求')['职位薪资'].mean())
        # print(new_df.groupby('学历要求')['职位薪资'].mean().index)
        mean = list(new_df.groupby('学历要求')['职位薪资'].mean())
        for i in range(len(mean)):
            mean[i] = int(mean[i])
        return {
            'degree': list(new_df.groupby('学历要求')['职位薪资'].mean().index),
            'mean': mean,
            'max': list(new_df.groupby('学历要求')['职位薪资'].max()),
            'min': list(new_df.groupby('学历要求')['职位薪资'].min())
        }

    # 对应岗位不同经验的最大薪资、最小薪资、平均薪资
    def get_salary_exp(self, key):
        new_df = self.df[self.df['职位名称关键字'] == key] # 提取对应关键字岗位的数据
        # print(new_df.groupby('工作经验')['职位薪资'].max())
        # print(new_df.groupby('工作经验')['职位薪资'].min())
        # print(new_df.groupby('工作经验')['职位薪资'].mean())
        # print(new_df.groupby('工作经验')['职位薪资'].mean().index)
        mean = list(new_df.groupby('工作经验')['职位薪资'].mean())
        for i in range(len(mean)):
            mean[i] = int(mean[i])
        return {
            'work_exp': list(new_df.groupby('工作经验')['职位薪资'].mean().index),
            'mean': mean,
            'max': list(new_df.groupby('工作经验')['职位薪资'].max()),
            'min': list(new_df.groupby('工作经验')['职位薪资'].min())
        }


data_analysis = DataAnalysis() # 单例模式

if __name__ == '__main__':
    # print(data_analysis.get_station_info('人工智能'))
    # print(data_analysis.get_station_info_citys('算法'))
    # print(data_analysis.get_house_price_citys())
    # print(data_analysis.get_salary_degree('信息安全'))
    # print(data_analysis.get_salary_exp('信息安全'))

    # 去重
    # df = pd.read_csv(FILE_ALL, encoding='utf-8')
    # print(df.columns)
    # df.info()
    # df.drop_duplicates()
    # df.info()
    # df.to_csv(FILE_ALL, encoding='utf-8', index=False)

    print(data_analysis.get_house_price('北京'))
    print(data_analysis.get_station_skill('后端开发'))