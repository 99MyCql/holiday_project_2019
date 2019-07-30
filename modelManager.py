'''
模型管理模块
'''
from sklearn.externals import joblib
from sklearn.preprocessing import LabelEncoder
from nlpModel.predict import CnnModel
import pickle

MODEL_FOLDER = 'sklearnModel/'

def key_handle(key):
    ret = key
    if key == '运维/技术支持':
        ret = '运维'
    if key == '电子/半导体':
        ret = '电子'
    return ret

def get_citys(key):
    model_le = MODEL_FOLDER + key_handle(key) + '_le.pkl'
    pkl_le = open(model_le, 'rb')
    le = pickle.load(pkl_le)
    pkl_le.close()
    return list(le.classes_)

def salary_pred(key, exp, degree, city):
    model = MODEL_FOLDER + key_handle(key) + '.pkl'
    model_le = MODEL_FOLDER + key_handle(key) + '_le.pkl'
    print(model_le)
    pkl_le = open(model_le, 'rb')
    le = pickle.load(pkl_le)
    pkl_le.close()
    city_index = list(le.classes_).index(city)
    degree_index = list(('中专','高中','大专','本科','硕士')).index(degree)
    Regression = joblib.load(model)
    pred = Regression.predict([[city_index, exp, degree_index]])
    return pred[0]

def station_recommend(msg):
    cnn_model = CnnModel()
    return cnn_model.predict(msg)


if __name__ == '__main__':
    print(salary_pred('后端开发', 2, '本科', '北京'))
    print(get_citys('后端开发'))
    # print(station_recommend('大专,0,java'))