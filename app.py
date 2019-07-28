from flask import Flask, render_template, url_for, jsonify, request
from datetime import timedelta
from dataManager import data_analysis

HOST = 'localhost'
PORT = 8080
PRODUCT = False # 是否开发环境

app = Flask(__name__)
app.debug = not PRODUCT # True 不能适用于开发环境，不安全
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

# 主界面
@app.route('/')
def home_page():
    station_list = []
    for key in data_analysis.keys:
        station_list.append(data_analysis.get_station_info(key))
    # print(station_list)
    return render_template('home.html', station_list = station_list, active_link = ['active', '', '', ''])

# 岗位详情界面
@app.route('/station_detail_page/<key>', methods=['GET'])
def station_detail_page(key):
    station_info = data_analysis.get_station_info(key)
    return render_template('station_detail.html', station_info = station_info, active_link = ['active', '', '', ''])

# 预测界面
@app.route('/predict_page')
def predict_page():
    return render_template('predict.html', keys = data_analysis.keys, active_link = ['', '', 'active', ''])

# 各网站岗位信息对比
@app.route('/api/get_website_comp')
def get_website_comp():
    list_51job = data_analysis.get_51job_stations_info()
    list_boss = data_analysis.get_51job_stations_info()
    list_51job_salary = []
    list_boss_salary = []
    for index in range(len(data_analysis.keys)):
        list_51job_salary.append(list_51job[index]['mean_salary'])
        list_boss_salary.append(list_boss[index]['mean_salary'])
    return jsonify({
        'keys': list(data_analysis.keys),
        'list_51job_salary': list_51job_salary,
        'list_boss_salary': list_boss_salary
    })

# 获取城市的信息，包括对应岗位数量分布信息、岗位薪资分布信息和房价
@app.route('/api/get_city_info/<key>')
def get_city_info(key):
    data = data_analysis.get_station_info_citys(key)
    city_list = data['city_list'] # 城市名列表
    count_city_list = data['count_city_list'] # 每个城市对应的岗位数量列表
    salary_city_list = data['salary_city_list'] # 每个城市对应的薪资平均值列表
    ret_count = []
    ret_salary = []
    for i in range(len(city_list)):
        # 为NaN
        if salary_city_list[i] != salary_city_list[i]:
            salary_city_list[i] = 0
        ret_count.append({
            'name': city_list[i],
            'value': int(count_city_list[i])
        })
        ret_salary.append({
            'name': city_list[i],
            'value': int(salary_city_list[i])
        })
    return jsonify({
        'count_list': ret_count,
        'salary_list': ret_salary,
        'house_price_list': data_analysis.get_house_price_citys()
    })

# 获取对应岗位不同学历/经验的薪资水平
@app.route('/api/get_salary_info/<key>')
def get_salary_info(key):
    return jsonify({
        'salary_degree': data_analysis.get_salary_degree(key),
        'salary_exp': data_analysis.get_salary_exp(key)
    })


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)