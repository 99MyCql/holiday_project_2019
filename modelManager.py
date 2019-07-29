from sklearn.externals import joblib
from sklearn.preprocessing import LabelEncoder as le
from nlpModel.predict import CnnModel

MODEL_FOLDER = 'skModel/'

def salary_pred(key, exp, degree, city):
    # city_index = list(le.classes_).index(city)
    # # job_index =  list(('前端开发','后端开发','移动开发','数据','测试','算法','运维/技术支持','硬件开发','通信','电子/半导体','项目管理','人工智能')).index(job)
    # degree_index = list(('中专','高中','大专','本科','硕士')).index(degree)
    # model = joblib.load(MODEL_FOLDER + key + '.pkl')
    # pred = Regression.predict([[job_index, exp, xueli_index]])
    # return pred
    return 9999

def station_recommend(msg):
    cnn_model = CnnModel()
    return cnn_model.predict(msg)


if __name__ == '__main__':
    print(salary_pred('后端开发', 2, '本科'))
    print(station_recommend('大专,0,java'))