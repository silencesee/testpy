# encoding: UTF-8
from pandas import Series, DataFrame
from config import *
import numpy as np
import pickle
import time, functools

# g_product_info_total = {'zn': ( 5, 5, 0.08, 3),
#                         'sn': ( 1, 10, 0.08, 3),
#                         'ru': ( 10, 5, 0.09, 12),
#                         'rb': ( 10, 1, 0.09, 6),
#                         'pb': ( 5, 5, 0.08, 3.5),
#                         'ni': ( 1, 10, 0.08, 12),
#                         'hc': ( 10, 1, 0.08, 6),
#                         'cu': ( 5, 10, 0.08, 12),
#                         'bu': ( 10, 2, 0.08, 4.6),
#                         'au': ( 1000, 0.05, 0.06, 10),
#                         'al': ( 5, 5, 0.08, 3),
#                         'ag': ( 15, 1, 0.07, 6),
#                         'y': (10, 2, 0.07, 5),
#                         'v': (5, 5, 0.07, 2),
#                         'pp': ( 5, 1, 0.07, 10),
#                         'p': (10, 2, 0.07, 5),
#                         'm': ( 10, 1, 0.07, 3),
#                         'l': ( 5, 5, 0.07, 4),
#                         'jm': ( 60, 0.5, 0.1, 43.2),
#                         'jd': (10, 1, 0.08, 12),
#                         'j': ( 100, 0.5, 0.1, 108),
#                         'i': (100, 0.5, 0.1, 22),
#                         'cs': ( 10, 1, 0.07, 3),
#                         'c': (10, 1, 0.07, 1.2),
#                         'a': (10, 1, 0.07, 4),
#                         'ZC': ( 100, 0.2, 0.08, 21),
#                         'WH': ( 20, 1, 0.07, 2.5),
#                         'TA': (5, 2, 0.06, 3),
#                         'SR': ( 10, 1, 0.05, 3),
#                         'SM': (5, 2, 0.08, 9),
#                         'SF': ( 5, 2, 0.08, 3),
#                         'RM': (10, 1, 0.08, 5),
#                         'OI': (10, 2, 0.08, 2.5),
#                         'MA': (10, 1, 0.08, 8),
#                         'FG': (20, 1, 0.08, 27),
#                         'CF': (5, 5, 0.08, 12),
#                         'TF': (10000, 0.005, 0.012, 6),
#                         'T': (10000, 0.005, 0.02, 3)
#                         }  # 品种属性表
# g_products = DataFrame(g_product_info_total, index=['instrument', 'unit', 'min_tick', 'margin', 'fee'])
# temp = [{'product': key, 'min15': None, 'min30': None, 'hour1': None, 'hour2': None, 'day': None} for key in
#         g_product_info_total.keys() if key in instruments]
# g_product_data = dict(zip(filter(lambda key: key in instruments, g_product_info_total.keys()), temp))  # 数据嵌套字典初始化
# g_products_select = g_products[instruments]
# contactUnit = g_products_select.loc['unit']
# contactMargin = g_products_select.loc['margin']
g_dt_index = {}  # 各周期的时间轴
# g_unit, g_min_tick, g_margin, g_fee = range(1, 5)
# g_min15, g_min30, g_hour1, g_hour2, g_day = range(1, 6)
# g_PeriodType = ['', 'min15', 'min30', 'hour1', 'hour2', 'day']
# g_buy, g_sell = range(1, 3)
# g_DirectionType = ['', 'buy', 'sell']
# g_open, g_close, g_close_today = range(1, 4)
# g_OffsetType = ['', 'open', 'close', 'close_today']
g_data = {'': None, 'min15': {}, 'min30': {}, 'hour1': {}, 'hour2': {}, 'day': {}}  # 在data模块里面被装入新的数据


class systemVars(object):
    contactInfo_total = {'zn': (5, 5, 0.08, 3),
                         'sn': (1, 10, 0.08, 3),
                         'ru': (10, 5, 0.09, 12),
                         'rb': (10, 1, 0.09, 6),
                         'pb': (5, 5, 0.08, 3.5),
                         'ni': (1, 10, 0.08, 12),
                         'hc': (10, 1, 0.08, 6),
                         'cu': (5, 10, 0.08, 12),
                         'bu': (10, 2, 0.08, 4.6),
                         'au': (1000, 0.05, 0.06, 10),
                         'al': (5, 5, 0.08, 3),
                         'ag': (15, 1, 0.07, 6),
                         'y': (10, 2, 0.07, 5),
                         'v': (5, 5, 0.07, 2),
                         'pp': (5, 1, 0.07, 10),
                         'p': (10, 2, 0.07, 5),
                         'm': (10, 1, 0.07, 3),
                         'l': (5, 5, 0.07, 4),
                         'jm': (60, 0.5, 0.1, 43.2),
                         'jd': (10, 1, 0.08, 12),
                         'j': (100, 0.5, 0.1, 108),
                         'i': (100, 0.5, 0.1, 22),
                         'cs': (10, 1, 0.07, 3),
                         'c': (10, 1, 0.07, 1.2),
                         'a': (10, 1, 0.07, 4),
                         'ZC': (100, 0.2, 0.08, 21),
                         'WH': (20, 1, 0.07, 2.5),
                         'TA': (5, 2, 0.06, 3),
                         'SR': (10, 1, 0.05, 3),
                         'SM': (5, 2, 0.08, 9),
                         'SF': (5, 2, 0.08, 3),
                         'RM': (10, 1, 0.08, 5),
                         'OI': (10, 2, 0.08, 2.5),
                         'MA': (10, 1, 0.08, 8),
                         'FG': (20, 1, 0.08, 27),
                         'CF': (5, 5, 0.08, 12),
                         'TF': (10000, 0.005, 0.012, 6),
                         'T': (10000, 0.005, 0.02, 3)
                         }  # 品种属性表

    def __init__(self, select_instruments):
        g_products = DataFrame(self.contactInfo_total, index=['unit', 'min_tick', 'margin', 'fee'])
        temp = [{'product': key, 'min15': None, 'min30': None, 'hour1': None, 'hour2': None, 'day': None} for key in
                self.contactInfo_total.keys() if key in instruments]
        self.dataContainer = dict(
            zip(filter(lambda key: key in select_instruments, self.contactInfo_total.keys()), temp))  # 数据嵌套字典初始化
        self.traderTaget = g_products[instruments]
        self._unit = np.array(self.traderTaget.loc['unit'], dtype=int)  # 品种每手吨数
        self._margin = np.array(self.traderTaget.loc['margin'], dtype=float)  # 保证金
        self._minmove = np.array(self.traderTaget.loc['min_tick'], dtype=int)  # 最小跳动点
        self._fee = np.array(self.traderTaget.loc['fee'], dtype=float)  # 手续费

    # def Unit(self):
    #     return self.g_products_select.loc['unit']

    @property
    def unit(self):
        return self._unit

    # def Margin(self):
    #     return self.g_products_select.loc['margin']

    @property
    def margin(self):
        return self._margin

    # def minmove(self):
    #     return self.g_products_select.loc['min_tick']

    @property
    def minmove(self):
        return self._minmove

    # def Fee(self):
    #     return self.g_products_select.loc['fee']

    @property
    def fee(self):
        return self._fee

        # @property
        # def

    def __getattr__(self, item):  # 兼容各种大小写
        item = item.lower().capitalize()
        item.replace
        return eval('self.' + item)


class trade_enum(object):
    Buy = 1
    Sell = 2
    Entry = 1
    Exit = 2
    Exit_today = 3

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
        self.time = timelist
        self.tradeNum = 0


# class Status(object):
#     def __init__(self, vol, entryPrice, exitPrice, barNum, orderTime):  # 初始化交易状态，用于临时转储
#         # bug 后续要添加变量检查，排除非向量数据进入
#         self.position = vol
#         self.entryPrice = entryPrice
#         self.exitPrice = exitPrice
#         self.tradeBar = barNum
#         self.orderTime = orderTime
#         pass


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
    size = np.shape(data)

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

    return newmat


def save(filepath, *varinput):
    with open(filepath, 'wb') as fp:
        for var in varinput:
            pickle.dump(fp, var)


#
# def save(filepath):
#     var = []
#     i = 0
#     with open(filepath, 'wb') as fp:
#         for var in varoytput:
#             var[i] = pickle.load(fp, var)
#             i += 1
#     return var


trade_enum = trade_enum()
contact = systemVars(instruments)
