from flask import Flask, render_template, url_for
from datetime import timedelta

HOST = 'localhost'
PORT = 8080
PRODUCT = False # 是否开发环境

app = Flask(__name__)
app.debug = not PRODUCT # True 不能适用于开发环境，不安全
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

@app.route('/')
def home():
    station_list = {
        
    }
    return render_template('home.html', station_list)

@app.route('/station')
def station():
    return render_template('station.html', station_name = '后端开发')

@app.route('/predict')
def predict():
    return render_template('predict.html')

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)