# encoding: UTF-8

import pandas as pd
import  numpy as np
from pandas import Series, DataFrame
from config import *
from globalVars import *


def load_data():  # 载入数据，支持多品种多周期同时载入
    date_parse = lambda dates: pd.datetime.strptime(dates, '%Y/%m/%d %H:%M')  # 读取分钟数据CSV时的时间列格式
    date_parse_day = lambda dates: pd.datetime.strptime(dates, '%Y/%m/%d')  # 读取日线数据CSV时的时间列格式
    for inst in instruments:
        for per in periods:
            if per == 'day':
                contact.dataContainer[inst][per] = pd.read_csv('./data/%s_%s.csv' % (inst, per), parse_dates=['date'],
                                                        date_parser=date_parse_day)
            else:
                contact.dataContainer[inst][per] = pd.read_csv('./data/%s_%s.csv' % (inst, per), parse_dates=['date'],
                                                        date_parser=date_parse)
                contact.dataContainer[inst][per].index = contact.dataContainer[inst][per].date  # 指定数据表的索引列
    return contact.dataContainer


def align_data(data):  # 按照时间索引重排序,数据结构：每个品种一个表，每个表中列索引为open、close...，行索引为时间
    for per in periods:  # 每一个周期序列分别重索引
        index = reduce(lambda a, b: a.append(b), (lambda a: [a[0][1][per].index])(data.items()))  # 去重处理
        index = index.unique()
        for inst in instruments:
            data[inst][per] = data[inst][per].reindex(index).sort_index()  # 按照时间索引重排序

        g_dt_index[per] = data[inst][per].index  # 刷新全局变量，各周期时间轴
    dataKeys = data[inst][per].keys()#输出行情数据因子矩阵
    timelist = list(g_dt_index[basic_period])#策略基频时间轴
    timelist.sort()  # 这里需要检查是否需要排序
    return timelist, dataKeys


def make_matrix(data):  # 数据矩阵化,重新修改了，索引直接可以使用g_dt_index[per]
    # g_data = {'': None, 'min15': {}, 'min30': {}, 'hour1': {}, 'hour2': {}, 'day': {}}
    #  bug 在载入多周期数据的时候，不能用同轴处理
    for per in periods:
        frame_close = DataFrame(index=g_dt_index[per])
        frame_open = DataFrame(index=g_dt_index[per])
        frame_high = DataFrame(index=g_dt_index[per])
        frame_low = DataFrame(index=g_dt_index[per])
        frame_volume = DataFrame(index=g_dt_index[per])
        frame_opi = DataFrame(index=g_dt_index[per])
        for inst in instruments:
            frame_close[inst] = data[inst][per].close
            frame_open[inst] = data[inst][per].open
            frame_high[inst] = data[inst][per].high
            frame_low[inst] = data[inst][per].low
            frame_volume[inst] = data[inst][per].volume
            frame_opi[inst] = data[inst][per].opi

        g_data[per]['close'] = np.array(frame_close)
        g_data[per]['open'] = np.array(frame_open)
        g_data[per]['high'] = np.array(frame_high)
        g_data[per]['low'] = np.array(frame_low)
        g_data[per]['vol'] = np.array(frame_volume)
        g_data[per]['opi'] = np.array(frame_opi)

    return
