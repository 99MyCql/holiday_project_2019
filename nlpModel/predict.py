# coding: utf-8

from __future__ import print_function

import os
import re
import numpy as np
import tensorflow as tf
import tensorflow.contrib.keras as kr
import jieba

from .cnn_model import TCNNConfig, TextCNN
from .data.job_loader import read_category, read_vocab

try:
    bool(type(unicode))
except NameError:
    unicode = str
    
# Variable embedding already exists, disallowed. 
# Did you mean to set reuse=True in VarScope? 
# Originally defined at:
# 遇到这种报错，只要在代码开头加上：tf.reset_default_graph()
#加入这句话，可以重新创建图，否则会报错
tf.reset_default_graph()

base_dir = 'nlpModel/data/job'
vocab_dir = os.path.join(base_dir, 'job_vocab.txt')

save_dir = 'nlpModel/checkpoints/textcnn'
save_path = os.path.join(save_dir, 'best_validation')  # 最佳验证结果保存路径


class CnnModel:
    def __init__(self):
        self.config = TCNNConfig()
        self.categories, self.cat_to_id = read_category()
        self.words, self.word_to_id = read_vocab(vocab_dir)
        self.config.vocab_size = len(self.words)
        self.model = TextCNN(self.config)

        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        saver.restore(sess=self.session, save_path=save_path)  # 读取保存的模型

    def predict(self, message):
        # 支持不论在python2还是python3下训练的模型都可以在2或者3的环境下运行
        content = unicode(message)
        data = [self.word_to_id[x] for x in content if x in self.word_to_id]

        feed_dict = {
            self.model.input_x: kr.preprocessing.sequence.pad_sequences([data], self.config.seq_length),
            self.model.keep_prob: 1.0
        }
        
        
        act = tf.nn.softmax(self.session.run(self.model.logits, feed_dict=feed_dict))
        #print('act = ', act)
        #print('type(act) = ', type(act))
        # 将 tensorflow 类型转换为 numpy
        act_np = act.eval(session=self.session)
        #print('type(act_np) = ', type(act_np))
        #print()
        #print('act_np:')
        #print(act_np)
        sub_max = np.argmax(act_np, axis=1)[0]
        sub_min = np.argmin(act_np, axis=1)[0]
        max = act_np[0][sub_max]
        act_np[0][sub_max] = act_np[0][sub_min]
        
        sub_max2 = np.argmax(act_np, axis=1)[0]
        max2 = act_np[0][sub_max2]
        act_np[0][sub_max2] = act_np[0][sub_min]
        
        sub_max3 = np.argmax(act_np, axis=1)[0]
        max3 = act_np[0][sub_max3]
        act_np[0][sub_max3] = act_np[0][sub_min]
        
        sub_max4 = np.argmax(act_np, axis=1)[0]
        act_np[0][sub_max] = max
        act_np[0][sub_max2] = max2
        act_np[0][sub_max3] = max3
        
        #print(sub_max, sub_max2, sub_max3, sub_max4)
        
        # 取前四大概率，筛去概率小于最大概率1/20的
        lis = []
        if (act_np[0][sub_max2] < act_np[0][sub_max] / 20.0):
            lis = [sub_max]
        elif (act_np[0][sub_max3] < act_np[0][sub_max] / 20.0):
            lis = [sub_max, sub_max2]
        elif (act_np[0][sub_max4] < act_np[0][sub_max] / 20.0):
            lis = [sub_max, sub_max2, sub_max3]
        else:
            lis = [sub_max, sub_max2, sub_max3, sub_max4]    
            
        #print(lis)
        
        #y_pred_cls = self.session.run(self.model.y_pred_cls, feed_dict=feed_dict)
        #print('y_pred_cls = ', y_pred_cls)
        
        res = []
        for i in range(len(lis)):
            res.append(self.categories[lis[i]])
        #print(res)
        return res


if __name__ == '__main__':
    
    """
    1、将文本划分为字词
    2、将字词分为中文、英文特征
    3、滤除特征表 ?n_set.txt 中没有的特征
    """
    
    cnn_model = CnnModel()
    test = 'Shanks,python,hello world JavaScript,HTML,CSS'
    print()
    print('输入文本：')
    print(test)
    print()
    
    print('输出一：')
    print(cnn_model.predict(test))
    print()
    """
    运行后输出结果为：
    ['前端开发', '测试', '移动开发', '后端开发']
    ['测试', '通信']
    ['测试', '移动开发']
    """
    
    str = test
    lis = jieba.lcut(str)
    lis = list(set(lis)) # list去重
    '''
    print()
    print('拆分文本[0]:')
    print(lis)
    print()
    '''
    
    en = []
    #cn = []
    
    for i in range(len(lis)):
        en_res = re.findall(r'\w+', lis[i], re.A)
        en_res = list(set(en_res)) # list去重
        for s1 in en_res:
            if not s1.isdigit():
                en.append(s1)
    '''            
    for i in range(len(lis)):
        # 去除字母数字
        ste = re.sub("[A-Za-z0-9\!\%\[\]\,\。]", "", lis[i])
        cn_res = jieba.lcut(ste)
        cn_res = list(set(cn_res)) # list去重
        for s2 in cn_res:
            cn.append(s2)
    '''
    
    # 停用词
    stopwords = [line.strip() for line in open('./dict/Stopword.txt',encoding='UTF-8').readlines()]
    
    en_data = []
    #cn_data = []
    
    for word in en:
        if word not in stopwords:
            if word != '\t':
                en_data.append(word)
    for i in range(len(en_data)):
        en_data[i] = en_data[i].capitalize()
    '''    
    for word2 in cn:
        if word2 not in stopwords:
            if word2 != '\t':
                cn_data.append(word2)
                
    print('cn_data:')
    print(cn_data)
    print()
    print('en_data:')
    print(en_data)
    print()
                
    with open('./dict/cn_set.txt',"r",encoding='UTF-8') as f1:
        cn_set = f1.read()
    cn_set = cn_set.split('\n')
    
    with open('./dict/en_set.txt',"r",encoding='UTF-8') as f2:
        en_set = f2.read()
    en_set = en_set.split('\n')
    '''
    
    with open('./dict/set.txt',"r",encoding='UTF-8') as f2:
        en_set = f2.read()
    en_set = en_set.split('\n')
    
    '''
    print('cn_set:')
    print(cn_set)
    print()
    print('en_set:')
    print(en_set)
    print()
    '''
        
    # 过滤元素
    cnt = 0
    for t2 in range(len(en_data)):
        if en_data[cnt] == ' ':
            en_data.remove(' ')
        elif en_data[cnt] == '':
            en_data.remove('')
        elif en_data[cnt] not in en_set:
            del en_data[cnt]
        else:
            cnt += 1
      
    '''
    cnt = 0
    for t in range(len(cn_data)):
        if cn_data[cnt] == ' ':
            cn_data.remove(' ')
        elif cn_data[cnt] == '':
            cn_data.remove('')
        elif (cn_data[cnt]) not in cn_set:
            del cn_data[cnt]
        else:
            cnt += 1
    '''
    '''
    print('英文特征:')
    print(en_data)
    print()
    print('中文特征:')
    print(cn_data)
    '''
    
    print('输出二：')
    print(en_data)