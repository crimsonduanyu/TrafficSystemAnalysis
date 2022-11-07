# -*- coding: utf-8 -*-            
# @Time : 2022/11/1 13:13
# @Author: 段钰
# @EMAIL： duanyu@bjtu.edu.cn
# @FileName: FlowStatCrawler.py
# @Software: PyCharm


import random
import urllib.request
import json
import re
import pandas as pd

import requests
import time

import matplotlib.pyplot as plt
import math

font = {'family': 'SimHei',
        'weight': 'bold',
        'size': '16'}

id = str(3186945861)  # input("请输入要爬取的微博uid：")
na = 'a'
ip_list = ['112.228.161.57:8118',
           '125.126.164.21:34592',
           '122.72.18.35:80',
           '163.125.151.124:9999',
           '114.250.25.19:80']

proxy_addr = '125.126.164.21:34592'


def use_proxy(url, proxy_addr):
    req = urllib.request.Request(url)
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36")
    proxy = urllib.request.ProxyHandler({'http': random.choice(ip_list)})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(req).read().decode('utf-8', 'ignore')
    return data


def get_containerid():
    url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id
    data = use_proxy(url, random.choice(ip_list))
    content = json.loads(data).get('data')
    for data in content.get("tabsInfo").get('tabs'):
        if data.get('tab_type') == 'weibo':
            containerid = data.get("containerid")
    return containerid


info_mat = pd.DataFrame(columns=['date', 'day_of_week', 'passenger_flow', 'ranks'])
most_used_station = pd.DataFrame(columns=["name"])
for i in range(20):
    weibo_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' \
                + id \
                + '&containerid=' \
                + get_containerid() \
                + '&page=' \
                + str(i)
    data = use_proxy(weibo_url, random.choice(ip_list))
    content = json.loads(data).get("data")
    cards = content.get('cards')
    print(len(cards))

    for card in cards:
        card_type = card.get("card_type")
        if card_type == 9:
            mblog = card.get("mblog")
            text = mblog.get("text")
            # print(text)
            try:
                date = re.findall('\d+月\d+日', text)[0]
                dayofweek = re.findall('周\S', text)[0]
                flow = re.findall('为(.*?)万乘次', text)[0]
                ranks = re.findall('依次为：(.*?)。', text)[0]
                ranks = ranks.split('、')
                info_mat.loc[len(info_mat)] = [date, dayofweek, flow, ranks]
                for i in ranks:
                    most_used_station.loc[len(most_used_station)] = i
            except:
                pass

info_mat.to_csv('近期客流数据.csv', index=False,encoding='utf-8')
most_used_station.drop_duplicates(inplace=True)
most_used_station.to_csv("most_used_stations.csv",index=False)
