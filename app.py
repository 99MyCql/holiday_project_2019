from flask import Flask, render_template, url_for, jsonify, request
from datetime import timedelta
from dataManager import data_analysis
import modelManager


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
@app.route('/station_detail_page', methods=['GET'])
def station_detail_page():
    key = request.args.get('key')
    station_info = data_analysis.get_station_info(key)
    return render_template('station_detail.html', station_info = station_info, active_link = ['active', '', '', ''])

# 预测界面
@app.route('/predict_page')
def predict_page():
    return render_template('predict.html',
            keys = data_analysis.keys,
            active_link = ['', '', 'active', ''])

# 预测
@app.route('/predict', methods=['POST'])
def predict():
    city = request.form.get('city')
    if city == '':
        return render_template('predict.html',
            data = request.form,
            keys = data_analysis.keys,
            msg = '没选择城市哦',
            active_link = ['', '', 'active', ''])

    station = request.form.get('station')
    if station == '':
        return render_template('predict.html',
            data = request.form,
            keys = data_analysis.keys,
            msg = '没选择岗位哦',
            active_link = ['', '', 'active', ''])

    degree = request.form.get('degree')
    if request.form.get('work_exp') == '':
        work_exp = 0
    else:
        work_exp = int(request.form.get('work_exp'))

    prediction = modelManager.salary_pred(station, work_exp, degree, city)
    print(prediction)
    house_price = data_analysis.get_house_price(city)
    return render_template('predict.html',
            data = request.form,
            keys = data_analysis.keys,
            prediction = round(prediction),
            house_price = house_price,
            active_link = ['', '', 'active', ''])

# 推荐界面
@app.route('/recommend_page')
def recommend_page():
    return render_template('recommend.html', active_link = ['', '', '', 'active'])

# 推荐
@app.route('/recommend', methods=['POST'])
def recommend():
    degree = request.form.get('degree')
    work_exp = request.form.get('work_exp')
    desc = request.form.get('desc')
    msg = degree + ',' + str(work_exp) + '年经验,' + desc
    res_list = modelManager.station_recommend(msg)
    return render_template('recommend.html',
            data = request.form,
            res_list = res_list,
            res_len = len(res_list),
            active_link = ['', '', '', 'active'])

# 各网站岗位信息对比
@app.route('/api/get_website_comp')
def get_website_comp():
    list_51job = data_analysis.get_51job_stations_info()
    list_boss = data_analysis.get_boss_stations_info()
    list_lagou = data_analysis.get_lagou_stations_info()
    list_51job_salary = []
    list_boss_salary = []
    list_lagou_salary = []
    for index in range(len(data_analysis.keys)):
        list_51job_salary.append(list_51job[index]['mean_salary'])
        list_boss_salary.append(list_boss[index]['mean_salary'])
        list_lagou_salary.append(list_lagou[index]['mean_salary'])
    return jsonify({
        'keys': list(data_analysis.keys),
        'list_51job_salary': list_51job_salary,
        'list_boss_salary': list_boss_salary,
        'list_lagou_salary': list_lagou_salary
    })

# 获取城市的信息，包括对应岗位数量分布信息、岗位薪资分布信息和房价
@app.route('/api/get_city_info')
def get_city_info():
    key = request.args.get('key')
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
@app.route('/api/get_salary_info')
def get_salary_info():
    key = request.args.get('key')
    return jsonify({
        'salary_degree': data_analysis.get_salary_degree(key),
        'salary_exp': data_analysis.get_salary_exp(key)
    })

# 获取对应岗位所需技能和占比
@app.route('/api/get_skill_info')
def get_skill_info():
    key = request.args.get('key')
    seriesData = data_analysis.get_station_skill(key)
    legendData = []
    for i in seriesData:
        legendData.append(i['name'])
    return jsonify({
        'legendData': legendData,
        'seriesData': seriesData
    })

# 获取对应岗位所需技能和占比
@app.route('/api/get_station_citys')
def get_station_citys():
    key = request.args.get('key')
    citys = modelManager.get_citys(key)
    return jsonify(citys)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)