# encoding: UTF-8
from pandas import DataFrame
from config import *
import numpy as np
import pandas as pd
import pickle

g_dt_index = {}  # 各周期的时间轴
g_data = {'': None, 'min15': {}, 'min30': {}, 'hour1': {}, 'hour2': {}, 'day': {}}  # 在data模块里面被装入新的数据


class systemVars(object):
    contactInfo_total = {'zn': (5, 5, 0.08, 3,'2007.03.26'),
                         'sn': (1, 10, 0.08, 3,'2015.03.27'),
                         'ru': (10, 5, 0.09, 12,'1999.01.01'),
                         'rb': (10, 1, 0.09, 6,'2009.03.27'),
                         'pb': (5, 5, 0.08, 3.5,'2011.03.24'),
                         'ni': (1, 10, 0.08, 12,'2015.03.27'),
                         'hc': (10, 1, 0.08, 6,'2014.03.21'),
                         'cu': (5, 10, 0.08, 12,'1993.01.01'),
                         'bu': (10, 2, 0.08, 4.6,'2013.10.09'),
                         'au': (1000, 0.05, 0.06, 10,'2008.01.09'),
                         'al': (5, 5, 0.08, 3,'1992.01.01'),
                         'ag': (15, 1, 0.07, 6,'2012.05.10'),
                         'y': (10, 2, 0.07, 5,'2006.01.09'),
                         'v': (5, 5, 0.07, 2,'2009.05.25'),
                         'pp': (5, 1, 0.07, 10,'2014.02.28'),
                         'p': (10, 2, 0.07, 5,'2007.10.29'),
                         'm': (10, 1, 0.07, 3,'2000.07.17'),
                         'l': (5, 5, 0.07, 4,'2007.07.31'),
                         'jm': (60, 0.5, 0.1, 43.2,'2013.03.22'),
                         'jd': (10, 1, 0.08, 12,'2013.11.08'),
                         'j': (100, 0.5, 0.1, 108,'2011.04.15'),
                         'i': (100, 0.5, 0.1, 22,'2013.10.18'),
                         'cs': (10, 1, 0.07, 3,'2014.12.19'),
                         'c': (10, 1, 0.07, 1.2,'2004.09.22'),
                         'a': (10, 1, 0.07, 4,'2001.03.15'),
                         'ZC': (100, 0.2, 0.08, 21,'2013.09.26'),
                         'WH': (20, 1, 0.07, 2.5,'2002.03.28'),
                         'TA': (5, 2, 0.06, 3,'2006.12.18'),
                         'SR': (10, 1, 0.05, 3,'2006.01.06'),
                         'SM': (5, 2, 0.08, 9,'2014.08.08'),
                         'SF': (5, 2, 0.08, 3,'2014.08.08'),
                         'RM': (10, 1, 0.08, 5,'2012.12.28'),
                         'OI': (10, 2, 0.08, 2.5,'2007.06.08'),
                         'MA': (10, 1, 0.08, 8,'2011.10.28'),
                         'FG': (20, 1, 0.08, 27,'2012.12.03'),
                         'CF': (5, 5, 0.08, 12,'2004.06.01'),
                         'IF': (300, 0.2, 0.012, 6,'2010.04.16'),
                         'TF': (10000, 0.005, 0.02, 3,'2015.02.09')
                         }  # 品种属性表

    def __init__(self, select_instruments):
        g_products = DataFrame(self.contactInfo_total, index=['unit', 'min_tick', 'margin', 'fee','born'])
        temp = [{'product': key, 'min15': None, 'min30': None, 'hour1': None, 'hour2': None, 'day': None} for key in
                self.contactInfo_total.keys() if key in instruments]
        # 数据嵌套字典初始化，实例化后，供后续data模块使用
        self.dataContainer = dict(
            zip(filter(lambda dkey: dkey in select_instruments, self.contactInfo_total.keys()), temp))
        self.databegin = dict(
            zip(filter(lambda dkey: dkey in select_instruments, self.contactInfo_total.keys()), temp))
        self.traderTaget = g_products[instruments]
        for name in g_products.index:  # 批量生产品种属性：每手吨数、保证金、最小跳动点、手续费
            if name=='born':
                object.__setattr__(self, '_' + name, np.array(self.traderTaget.loc[name]))
                self._born = pd.to_datetime(self._born)
            else:
                object.__setattr__(self, '_' + name, np.array(self.traderTaget.loc[name], dtype=float))
            print '初始化 '+name

    @property
    def unit(self):
        return self._unit

    @property
    def margin(self):
        return self._margin

    @property
    def minmove(self):
        return self._minmove

    @property
    def fee(self):
        return self._fee

    @property
    def born(self):
        return self._born
    def __getattr__(self, item):  # 兼容各种大小写
        item = item.lower().capitalize()

        return eval('self.' + item)


class Recorder(object):
    def __init__(self, timelist):  # 初始化交易记录，用于绩效分析，每一个属性是一个dataFrame
        size = (len(timelist), len(instruments))

        self.holdingPrice = np.zeros(size)
        self.exitPrice = np.zeros(size)
        self.holdingLots = np.zeros(size)
        self.exitLots = np.zeros(size)
        self.traded = np.full(size, False, dtype=bool)
        self.time = timelist
        self.tradeNum = 0


def findmax(data):
    maxdata = np.nanmax(data)
    location = data == maxdata

    return maxdata, location


def findmin(data):
    mindata = np.nanmin(data)
    location = data == mindata

    return mindata, location


def floor(data):
    if isinstance(data, np.ndarray):
        try:
            return np.floor(data)
        except:
            data = np.array(data, dtype=float)
            return np.floor(data)
    else:
        return floor(data)


def shift(data, x, y, *replace):  # 矩阵平移，以坐标轴同向，x为正表示水平右移，y为正表示垂直上移
    if type(data) != np.ndarray:
        raise TypeError
    size = np.shape(data)
    if data.dtype == bool:
        print '不支持布尔数组'
        raise TypeError
    if np.ndim(data) == 2:
        m = size[0]
        n = size[1]
        newmat = np.full(size, np.nan)
        if len(replace) == 0:
            replace = np.nan
        if type(x) != int or type(y) != int:
            raise TypeError
        if x > 0:
            x2 = slice(x, n)
            x1 = slice(0, n - x)
        else:
            x2 = slice(0, n + x)
            x1 = slice(0 - x, n)

        if y > 0:
            y2 = slice(0, m - y)
            y1 = slice(y, m)
        else:
            y2 = slice(-y, m)
            y1 = slice(0, m + y)
        newmat[y2, x2] = data[y1, x1]
    else:
        n = size[0]
        newmat = np.full(size, np.nan)
        dx = max(abs(x), abs(y))  # 一维向量python默认是以行形式存在，不论修改x还是y效果都一样,这里兼容考虑有时候以为一维向量以列形式出现
        if type(x) != int or type(y) != int:
            raise TypeError
        if x > 0:
            x2 = slice(dx, n)
            x1 = slice(0, n - dx)
        else:
            x2 = slice(0, n + dx)
            x1 = slice(0 - dx, n)
        newmat[x2] = data[x1]
    return newmat


def save(filepath, *varinput):
    with open(filepath, 'wb') as fp:
        for var in varinput:
            pickle.dump(fp, var)


contact = systemVars(instruments)
