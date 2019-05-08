# encoding: utf-8
import json
import graphlab
import pandas as pd
import jieba
import numpy as np


# 封装基础返回数据
def res_success(data=""):
    result = {}
    result["message"] = "success"
    result["code"] = 1
    result["data"] = data
    return json.dumps(result, ensure_ascii=False)


# 封装基础返回数据
def res_fail(data=""):
    result = {}
    result["message"] = "fail"
    result["code"] = -1
    result["data"] = data
    return json.dumps(result, ensure_ascii=False)


# 根据模型获取所有的推荐
knn_model = graphlab.load_model("knn_model")
datas = graphlab.SFrame.read_csv('./article.csv')
word_count = graphlab.text_analytics.count_words(datas['content'])
datas['word_count'] = word_count
tfidf = graphlab.text_analytics.tf_idf(datas['word_count'])
datas['tfidf'] = tfidf  # 将计算出来的tfidf赋给语料库
def get_recommond_ids(data):
    # 计算对应的权值
    duration_sum = sum(int(d['duration']) for d in data)
    print(data)

    recommonds = []
    for item in data:
        item_weight = format(float(item['duration']) / duration_sum, '.1f')
        print(item_weight)
        categoryId = int(item['categoryId'])
        size = int(float(item_weight) * 10 + 2)
        if(datas[datas['id'] == categoryId]):
             result = knn_model.query(datas[datas['id'] == categoryId], k=size)
             result = result.to_dataframe().to_json()
             result = json.loads(result)['reference_label']
             for key, value in result.items():
                if key == '0':
                    continue
                else:
                    recommonds.append(value)
    recommonds = list(set(recommonds))         
    return recommonds


# 训练模型
def train_model():
    train_data = graphlab.SFrame.read_csv('./article.csv')
    train_data['word_count'] = graphlab.text_analytics.count_words(train_data['content'])
    train_tfidf = graphlab.text_analytics.tf_idf(train_data['word_count'])
    train_data['tfidf'] = train_tfidf  # 将计算出来的tfidf赋给语料库
    model = graphlab.nearest_neighbors.create(train_data, features=['tfidf'], label='id')
    model.save('knn_model')


# 清洗数据
def clearning_data():
    file_path = '/Users/yanglin/Desktop/yl/c++/arcsoft-arcface/face-api/script/articles.txt'
    file = open(file_path)

    new_data = []
    for line in file:
        test = line.split('@@@')
        test[1] = test[1].replace('"', '')
        if len(test[2]) <= 500:
            continue

        # 替换标点为空格，替换回车符等
        test[2] = test[2].replace('"', '').replace('\\n', ' ').replace('，', ' ') \
            .replace('、', ' ').replace('。', ' ').replace('\\t', '').replace(',', ' ') \
            .replace('\n', ' ')

        # 进行中文分词
        result = jieba.lcut(test[2], cut_all=True)
        result = ' '.join(result)

        new_data.append([
            test[0],
            test[1],
            result
        ])
    name = ['id', 'title', 'content']
    p_frame = pd.DataFrame(columns=name, data=new_data)
    p_frame.to_csv('article.csv', encoding='utf-8')
