from flask import Flask, render_template, url_for
from datetime import timedelta
from data.dataManager import data_analysis

HOST = 'localhost'
PORT = 8080
PRODUCT = False # 是否开发环境

app = Flask(__name__)
app.debug = not PRODUCT # True 不能适用于开发环境，不安全
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

@app.route('/')
def home():
    station_list = []
    for key in data_analysis.keys:
        station_list.append(data_analysis.get_station_info(key))
    # print(station_list)
    return render_template('home.html', station_list = station_list)

@app.route('/station_detail')
def station_detail():
    station_info = data_analysis.get_station_info('后端开发')
    return render_template('station_detail.html', station_info = station_info)

@app.route('/predict')
def predict():
    return render_template('predict.html')

# @app.route('/api/get')
# def home():
#     station_list = []
#     for key in data_analysis.keys:
#         station_list.append(data_analysis.get_station_info(key))
#     # print(station_list)
#     return render_template('home.html', station_list = station_list)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)