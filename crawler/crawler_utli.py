'''
用于爬虫的工具类
'''
import requests
import random
from bs4 import BeautifulSoup

# 返回一个随机的请求头 headers
def getHeaders():
    user_agent_list = [ \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    UserAgent = random.choice(user_agent_list)
    return {
        'User-Agent': UserAgent
    }

IP_LIST = [] # 代理ip列表
IP_LIST_INDEX = 100 # ip列表索引

def changeProxies():
    global IP_LIST, IP_LIST_INDEX
    print(IP_LIST_INDEX, ': ', IP_LIST[IP_LIST_INDEX][:-1], ' is useless')
    IP_LIST_INDEX += 1

# 验证该ip是否可用
def verify_IP(ip, headers):
    proxies = {"http": ip}
    url = "http://www.baidu.com/"
    try:
        req = requests.get(url, headers=headers, proxies=proxies, timeout=3)
        if req.status_code == 200:
            return True
        else:
            return False
    except requests.RequestException as e:
        print("IP" + ip + "不可用 :")
        print(e)
        return False

# 获取代理IP
def getProxies():
    global IP_LIST, IP_LIST_INDEX
    if len(IP_LIST) == 0:
        with open('ip.txt', 'r') as f:
            IP_LIST = f.readlines()
    while True:
        ip = IP_LIST[IP_LIST_INDEX][:-1]
        if verify_IP(ip, getHeaders()):
            break
        else:
            changeProxies()
    print(IP_LIST_INDEX, ': ', ip)
    return {
        'http': 'http://' + ip,
        'https': 'https://' + ip
    }

if __name__ == '__main__':
    print(getProxies())
    changeProxies()
    getProxies()
