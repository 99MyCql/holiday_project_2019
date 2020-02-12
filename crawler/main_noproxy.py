# -*- coding: utf-8 -*-
'''
爬取boss直聘网的互联网相关岗位数据
慢一点才能快一点
'''
import requests
import random
import time
import csv
from lxml import etree
from retrying import retry

FILE = 'jobs.csv'
KEYS = [
    '职位名称',
    '职位名称关键字',
    '职位薪资',
    '公司名称',
    '地区',
    '工作经验',
    '学历要求',
    '职位描述要求',
]
KEYWORDS = [
    '后端开发',     # 0
    '移动开发',     # 1
    '测试',         # 2
    '运维/技术支持', # 3
    '数据',         # 4
    '项目管理',     # 5
    '硬件开发',     # 6
    '前端开发',     # 7
    '通信',         # 8
    '电子/半导体',  # 9
    '人工智能',     # 10
    '信息安全',     # 11
    '算法'         # 12
]

# 将职位信息保存到csv文件
def save_to_csv(job):
    with open(FILE, 'a', encoding='utf-8') as f:
        csv_writer = csv.DictWriter(f, KEYS)
        # 将岗位信息保存到csv文件中
        csv_writer.writerows([job])


# 返回一个随机的请求头 headers
def getHeaders():
    user_agent_list = [
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
    ]
    UserAgent = random.choice(user_agent_list)
    return {
        'User-Agent': UserAgent
    }


# 根据关键字进行搜索，并爬取结果
def get_page(page_id, keyword):
    print('-'*20 + '>' + 'get_page()')
    url = 'https://www.zhipin.com/c100010000/?query={k}&page={page_id}&ka=page-{page_id}'.format(page_id=page_id, k=keyword)
    response = requests.get(url, headers=getHeaders())
    print(response.status_code)
    if response.status_code == 403:
        exit(0)
    return response.text


# 进入职位详情页面爬取职位要求描述
@retry(wait_fixed=8000, stop_max_attempt_number=10) # 当raise异常时，循环调用该函数(最多100次，每次循环间隔8秒)
def get_job_detail(link):
    print('-'*20 + '>' + 'get_job_detail()')
    response = requests.get(link, headers=getHeaders())
    data = etree.HTML(response.text)
    # 检验是否出现验证码
    tips = data.xpath('/html/head/title/text()')
    tips_title = 'BOSS直聘验证码'
    if tips[0] == tips_title:
        # 休息休息一下
        timewait = random.randint(60, 80)
        print('出现验证码，等待', timewait, '秒')
        time.sleep(timewait)
        raise NameError # 引发NameError来进行函数循环

    job_desc = data.xpath('//*[@id="main"]/div[3]/div/div[2]/div[2]/div[1]/div/text()')
    jd = "".join(job_desc).strip()
    return jd


# 对html页面进行解析，爬取岗位数据并返回
def parse_page(html, keyword, page_id):
    print('-'*20 + '>' + 'parse_page()')
    # 观察数据结构可得
    data = etree.HTML(html)
    if page_id == 1:
        items = data.xpath('//*[@id="main"]/div/div[3]/ul/li')
    else:
        items = data.xpath('//*[@id="main"]/div/div[2]/ul/li')
    for item in items:
        job_district = item.xpath('./div/div[1]/p/text()[1]')[0] # 岗位地区
        job_link = item.xpath('./div/div[1]/h3/a/@href')[0] # 岗位详情链接
        job_name = item.xpath('./div/div[1]/h3/a/div[1]/text()')[0] # 岗位名字
        job_salary = item.xpath('./div/div[1]/h3/a/span/text()')[0] # 岗位薪资
        job_company = item.xpath('./div/div[2]/div/h3/a/text()')[0] # 岗位公司
        job_experience = item.xpath('./div/div[1]/p/text()[2]')[0] # 岗位要求工作经验
        try:
            job_degree = item.xpath('./div/div[1]/p/text()[3]')[0] # 岗位要求学历
        except IndexError:
            job_degree = '无'
        job_link = 'https://www.zhipin.com' + job_link
        print(job_link)
        # 获取职位描述
        job_detail = get_job_detail(job_link)
        job = {
            '职位名称': job_name,
            '职位名称关键字': keyword,
            '职位薪资': job_salary,
            '公司名称': job_company,
            '地区': job_district,
            '工作经验': job_experience,
            '学历要求': job_degree,
            '职位描述要求': job_detail,
        }
        print(job)
        save_to_csv(job)
        # 休息休息一下
        timewait = random.randint(20, 25)
        print('获取到一个岗位信息，等待', timewait, '秒')
        time.sleep(timewait)


if __name__ == '__main__':
    # 获取上一次进行到哪一个关键字的哪一页
    with open('step.txt', 'r', encoding='utf-8') as f:
        step_i = int(f.readline())
        step_j = int(f.readline())
    print(step_i, step_j)

    # 遍历所有关键字
    for i in range(step_i, len(KEYWORDS)):
        # 遍历所有结果页
        for j in range(step_j, 11):
            # 将当前进行到哪一步保存下来
            with open('step.txt', 'w', encoding='utf-8') as f:
                f.write(str(i))
                f.write('\n')
                f.write(str(j))

            print('-' * 66)
            print('正在爬取"{k}"关键字的第{page_id}页'.format(k=KEYWORDS[i], page_id=j))

            # 爬取页面
            html = get_page(j, KEYWORDS[i])
            # print(html)

            # 休息休息一下
            timewait = random.randint(20, 25)
            print('get_page()结束，等待', timewait, '秒')
            time.sleep(timewait)

            # 解析页面，并将爬取的职位信息数据保存到csv文件
            print('正在解析页面中的数据')
            parse_page(html, KEYWORDS[i], j)

            # 休息休息一下
            timewait = random.randint(20, 25)
            print('parse_page()结束，等待', timewait, '秒')
            time.sleep(timewait)

        step_j = 1 # 让下一个关键字从第1页开始
        # 休息休息一下
        timewait = random.randint(200, 300)
        print('爬取完一个页面，等待', timewait, '秒')
        time.sleep(timewait)

    file.close()