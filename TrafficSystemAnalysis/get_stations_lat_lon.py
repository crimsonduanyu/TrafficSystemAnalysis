# -*- coding: utf-8 -*-            
# @Time : 2022/11/1 22:10
# @Author: 段钰
# @EMAIL： duanyu@bjtu.edu.cn
# @FileName: get_stations_lat_lon.py
# @Software: PyCharm
import pandas as pd
import numpy as np
import json
import csv
import sys
import time
import re
import requests

#  stations = pd.read_csv('most_used_stations.csv')
stations = pd.read_csv('station_data/武汉地铁站大全.csv')
stations = stations.to_numpy().ravel()
stations = list(stations)

ak = 'd55Hb1IIUFsocvPFIWl1sStvG1hEfNrG'
geo_url_list = []

for station in stations:
    geo_url = 'https://api.map.baidu.com/geocoding/v3/?address=' + str(
        station) + '&output=json&ak=' + ak + '&callback=showLocation'
    geo_url_list.append(geo_url)

data = pd.DataFrame(columns=['lon', 'lat'])

for url in geo_url_list:
    time.sleep(0.12)  # 为了防止并发量报警，设置了一个休眠。
    print(url)
    try:
        html = requests.get(url)  # 获取网页信息
        content = html.content
        content = str(content)
        usable_content = re.findall('{\"lng\":+\d+.+\d+,\"lat\":+\d+.+\d+\d+}', content)[0]
        lon = usable_content.split(',')[0][7:]
        lat = usable_content.split(',')[1][6:-1]
        data.loc[len(data)] = [lon, lat]
    except:
        data.loc[len(data)] = [None, None]
    #  print(data)

stat_mat = pd.DataFrame(columns=['name', 'lon', 'lat'])
for i in range(len(stations)):
    stat_mat.loc[i] = [stations[i], data.loc[i, 'lon'], data.loc[i, 'lat']]

stat_mat.to_csv("all地铁站经纬度.csv", index=False)
