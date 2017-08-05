# encoding: UTF-8

import pandas as pd
from pandas import Series, DataFrame
from config import *

g_products = DataFrame(g_product_info, index=['instrument', 'unit', 'min_tick', 'margin', 'fee'])

# g_product_data = {}
g_dt_index = {}


g_unit, g_min_tick, g_margin, g_fee = range(1, 5)
g_min15, g_min30, g_hour1, g_hour2, g_day = range(1, 6)
g_PeriodType = ['', 'min15', 'min30', 'hour1', 'hour2', 'day']

g_buy, g_sell = range(1, 3)
g_DirectionType = ['', 'buy', 'sell']

g_open, g_close, g_close_today = range(1, 4)
g_OffsetType = ['', 'open', 'close', 'close_today']

g_data = {'': None, 'min15': {}, 'min30': {}, 'hour1': {}, 'hour2': {}, 'day': {}}


def load_data():  # 载入数据，支持多品种多周期同时载入

    temp = [{'product': key, 'min15': None, 'min30': None, 'hour1': None, 'hour2': None, 'day': None} for key in
            g_product_info.keys() if key in instruments]
    g_product_data = dict(zip(filter(lambda key: key in instruments, g_product_info.keys()), temp))  # 数据嵌套字典初始化

    date_parse = lambda dates: pd.datetime.strptime(dates, '%Y/%m/%d %H:%M')  # 读取分钟数据CSV时的时间列格式
    date_parse_day = lambda dates: pd.datetime.strptime(dates, '%Y/%m/%d')  # 读取日线数据CSV时的时间列格式
    for inst in instruments:
        if g_product_data.has_key(inst):
            for per in periods:
                if per == 'day':
                    g_product_data[inst][per] = pd.read_csv('./data/%s_%s.csv' % (inst, per), parse_dates=['date'],
                                                            date_parser=date_parse_day)
                else:
                    g_product_data[inst][per] = pd.read_csv('./data/%s_%s.csv' % (inst, per), parse_dates=['date'],
                                                            date_parser=date_parse)
                g_product_data[inst][per].index = g_product_data[inst][per].date  # 指定数据表的索引列
    return g_product_data


def align_data(data):  # 按照时间索引重排序
    global  g_dt_index

    for per in periods:  # 每一个周期序列分别重索引
        index = reduce(lambda a, b: a.append(b), (lambda a: [a[0][1][per].index])(data.items()))  # 去重处理
        index = index.unique()
        for inst in instruments:
            data[inst][per] = data[inst][per].reindex(index).sort_index() # 按照时间索引重排序
        g_dt_index[per]=index



def make_martrix(data):  # 数据矩阵化,重新修改了，索引直接可以使用g_dt_index[per]
    global g_dt_index
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

        g_data[per]['close'] = frame_close
        g_data[per]['open'] = frame_open
        g_data[per]['high'] = frame_high
        g_data[per]['low'] = frame_low
        g_data[per]['volume'] = frame_volume
        g_data[per]['opi'] = frame_opi
