#!/usr/bin/env python
# -*- coding:utf-8 _*-
__author__ = 'LJjia'
# *******************************************************************
#     Filename @  draw_scatter.py
#       Author @  Jia Liangjun
#  Create date @  2020/02/06 11:38
#        Email @  LJjiahf@163.com
#  Description @  python画动态散点图
# ********************************************************************

import numpy as np  # 数组相关的库
import matplotlib.pyplot as plt  # 绘图库
import time
from pylab import mpl

# 设置字体
mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题




# 总共的人数统计
sum_of_human = 2000
# 潜伏期 表示患者感染上病毒后多少天才患病
incubation_period = 40
# 诊疗意愿，患者发病后多少天去医院
treat_willingness=40
isolation_all_day=incubation_period+treat_willingness
# 可容纳的隔离数
isolation_pos = 400
# 感染范围
infection_area = 0.02
# 运动范围参数 0-1
move_area_param =0.3
# 初始感染者
first_infected_cnt = 10











# 生成画布
plt.figure(figsize=(18, 14), dpi=80)
plt.ion()


def get_normal_list(mu=0.0, sigma=0.7, sampleNo=sum_of_human, seed=0):
    '''
    :param mu: 对称轴
    :param sigma: 方差
    :param sampleNo: 样点个数
    :return:
    '''
    if seed:
        np.random.seed(seed)
    else:
        np.random.seed(round(time.time() * 100000) % 10000)
    if sigma < 0:
        sigma = 0
    s = np.random.normal(mu, sigma, sampleNo)
    return s


x1 = get_normal_list(seed=1, sampleNo=int(sum_of_human / 2))
x2 = get_normal_list(seed=2, sampleNo=int(sum_of_human / 2))
x = get_normal_list(seed=3, sampleNo=sum_of_human)
y1 = get_normal_list(seed=5, sampleNo=int(sum_of_human / 2))
y2 = get_normal_list(seed=6, sampleNo=int(sum_of_human / 2))

np.random.seed(10)
first_infected_cnt_index = np.random.randint(0, sum_of_human, size=first_infected_cnt)
infected_index_set = set(first_infected_cnt_index)
infected_index_history = []
infected_index_history.append(infected_index_set)
print('初始感染者', infected_index_set)
# 初始化相关变量
isolation_set=set()
plt_x_isolation=np.array([])
plt_y_isolation = np.array([])
plt_x_sick=np.array([])
plt_y_sick=np.array([])

move_mu = 0
move_sigma = 0.01*move_area_param
for day in range(1, 1000):
    plt.cla()
    plt.grid(False)
    # 人员运动
    move_x1 = get_normal_list(mu=move_mu , sigma=move_sigma, sampleNo=int(sum_of_human / 2))
    move_x2 = get_normal_list(mu=-move_mu , sigma=move_sigma, sampleNo=int(sum_of_human / 2))
    move_y1 = get_normal_list(mu=move_mu , sigma=move_sigma, sampleNo=int(sum_of_human / 2))
    move_y2 = get_normal_list(mu=-move_mu , sigma=move_sigma, sampleNo=int(sum_of_human / 2))
    x1 = x1 + move_x1
    x2 = x2 + move_x2
    y1 = y1 + move_y1
    y2 = y2 + move_y2

    plt_x = np.concatenate((x1, x2), axis=0)
    plt_y = np.concatenate((y1, y2), axis=0)

    set_infected_index_today=set()
    for infected_index in infected_index_set:
        infected_point = (plt_x[infected_index], plt_y[infected_index])
        infected_array_index_today = np.where(
            (plt_x > infected_point[0] - infection_area) & (plt_x < infected_point[0] + infection_area) \
            & (plt_y > infected_point[1] - infection_area) & (plt_y < infected_point[1] + infection_area))
        infected_array_index_today=infected_array_index_today[0]
        set_infected_index_today=set_infected_index_today|set(infected_array_index_today)

    # 记录当天之后感染的所有人 set 和历史感染set的统计集合list
    infected_index_set = infected_index_set | set_infected_index_today
    infected_index_history.append(infected_index_set)

    # 已经在潜伏期的人数
    plt_x_infection=plt_x[list(infected_index_set)]
    plt_y_infection=plt_y[list(infected_index_set)]
    # 已出现病症的人数
    if day>=incubation_period:
        plt_x_sick=plt_x[list(infected_index_history[day-incubation_period])]
        plt_y_sick = plt_y[list(infected_index_history[day - incubation_period])]
    # 隔离人数
    if day>=isolation_all_day:

        if len(isolation_set)<isolation_pos:
            # print(len(isolation_set))
            isolation_set=isolation_set|infected_index_history[day-isolation_all_day]
        infected_index_set=infected_index_set-isolation_set
        plt_x_isolation = plt_x[list(isolation_set)]
        plt_y_isolation = plt_y[list(isolation_set)]

    # 设置坐标轴范围 关闭坐标轴显示
    plt.xlim((-2, 2))
    plt.ylim((-2, 2))
    plt.axis('off')
    # 正常人
    plt.scatter(plt_x, plt_y, alpha='0.7', marker='.',label='正常人')  # 绘制散点图，透明度为0.6（这样颜色浅一点，比较好看）

    # 潜伏期人
    plt.scatter(plt_x_infection, plt_y_infection, c='yellow',alpha='0.7', marker='.',label='潜伏期')
    # 患病人
    if day >= incubation_period:
        plt.scatter(plt_x_sick, plt_y_sick, c='red', alpha='0.8', marker='.',label='发病')
    # 隔离人
    if day >= isolation_all_day:
        plt.scatter(plt_x_isolation, plt_y_isolation, c='white', marker='.')

    plt.legend(loc='upper right')
    plt.pause(0.0001)
