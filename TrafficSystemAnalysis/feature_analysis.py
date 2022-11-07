# -*- coding: utf-8 -*-            
# @Time : 2022/11/3 10:30
# @Author: 段钰
# @EMAIL： duanyu@bjtu.edu.cn
# @FileName: feature_analysis.py
# @Software: PyCharm
import sys
from sklearn.model_selection import train_test_split
from sklearn import tree
import matplotlib.pyplot as plt
import os
import pydotplus
import pandas as pd

print('Python %s on %s' % (sys.version, sys.platform))

os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

data = pd.read_csv('station_data/poi_with_label_for_all.csv')
data.drop(columns=['Station_Name'], inplace=True)

X = data.loc[:,
    ['美食', '酒店', '购物', '生活服务', '丽人', '旅游景点', '休闲娱乐', '运动健身', '教育培训', '其他', '文化传媒', '医疗', '汽车服务', '交通设施', '金融', '房地产',
     '公司企业', '政府机构', '出入口', '自然地物', '行政地标', '门址']]
y = data.loc[:, 'label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)

session = tree.DecisionTreeClassifier(criterion='gini')
session = session.fit(X_train, y_train)

accuracy = session.score(X_test, y_test)

feature_name = ['美食', '酒店', '购物', '生活服务', '丽人', '旅游景点', '休闲娱乐', '运动健身', '教育培训', '其他', '文化传媒', '医疗', '汽车服务', '交通设施',
                '金融', '房地产',
                '公司企业', '政府机构', '出入口', '自然地物', '行政地标', '门址']

dot_data = tree.export_graphviz(session, out_file=None,
                                feature_names=feature_name,
                                class_names=['较低客流量', '极高客流量'])
dot_data_val = dot_data
dot_data_val = dot_data_val.replace('helvetica', 'MicrosoftYaHei')
graph = pydotplus.graph_from_dot_data(dot_data_val)
graph.write_pdf(r'Visualize\Original.pdf')

path = session.cost_complexity_pruning_path(X_train, y_train)
ccp_alphas, impurities = path.ccp_alphas, path.impurities
print('ccp_alphas:', ccp_alphas)
print('impurities', impurities)

print("未剪枝时，正确率为:", accuracy)
acc_stat = []
acc_stat.append(accuracy)

for i in range(1, len(ccp_alphas)):
    session = tree.DecisionTreeClassifier(criterion='gini', ccp_alpha=ccp_alphas[i] + 1e-6)
    session = session.fit(X_train, y_train)
    accuracy = session.score(X_test, y_test)
    acc_stat.append(accuracy)
    print("===================================================")
    print("设置alpha={}\n剪枝后的树不纯度：{}\n此时的模型准确率：{}".
          format(ccp_alphas[i], impurities[i], accuracy))
    dot_data = tree.export_graphviz(session, out_file=None,
                                    feature_names=feature_name,
                                    class_names=['较低客流量', '极高客流量'])
    dot_data_val = dot_data
    dot_data_val = dot_data_val.replace('helvetica', 'MicrosoftYaHei')
    graph = pydotplus.graph_from_dot_data(dot_data_val)
    graph.write_pdf(r'Visualize\CUT' + str(i) + '.pdf')

print('各步骤的剪枝决策树可视化图已经保存到：Visualize/')
print("Prosess Terminated")

plt.plot(ccp_alphas, acc_stat, marker='o')
plt.xlabel("Value of CCP_ALPHA")
plt.ylabel("Accuracy")
plt.show()
