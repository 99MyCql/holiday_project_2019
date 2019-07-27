'''
通过boss直聘网，爬取与互联网相关的关键字
'''
import requests
from crawler_utli import getHeaders
import json

# 如果data存在子项，就遍历子项；若不存在子项，就追加data中的name字段到keywords中
# def getSubModelList(keywords, data):
#     if not data['subLevelModelList']:
#         keywords.append(data['name'])
#     else:
#         if data['name'] == '通信' or data['name'] == '电子/半导体' or data['name'] == '软件销售支持':
#             return
#         for i in data['subLevelModelList']:
#             getSubModelList(keywords, i)

# 爬取关键字json文件保存到本地
def getKeywords():
    url = 'https://www.zhipin.com/wapi/zpCommon/data/position.json'
    headers = getHeaders()
    resp = requests.get(url, headers=headers)
    json_resp = json.loads(resp.text)
    # print(json_resp['zpData'][1])
    keywords = []
    for i in json_resp['zpData'][1]['subLevelModelList']:
        keywords.append(i['name'])
    return keywords

if __name__ == '__main__':
    keywords = getKeywords()
    print(keywords)
    with open('keywords.txt', 'w', encoding='utf-8') as f:
        for i in keywords:
            f.write(i)
            f.write('\n')