# encoding: UTF-8

from basic_class import IStrategy
from data import *
import math
import numpy as np
import pandas as pd
from analysis import *
np.seterr(invalid='ignore')  # 忽略nan比较时的警告


class StrategyTog(IStrategy):  # 策略实例，继承自策略基类

    def __init__(self):# 策略运行参数
        super(StrategyTog, self).__init__()  # 调用父类方法
        self._lastHighPrice = {}
        self._lastLowPrice = {}
        self.diff = (np.array(self.close[1:])- np.array(self.close[0:-1])) / np.array(self.close[0:-1])
    def __str__(self):
        pass

    @property
    def period(self):
        return self._period

    def init_params(self):#策略逻辑参数
        self._params['follow_stop'] = 0.01
        self._params['nan_rate'] = 0.4
        self._params['majority_rate'] = 0.9  # 设置全市场共振阀值
        self._params['money'] = 100000

    def loop(self, pos):
        if pos > 2:

            if len(self._tradeLog) > 0:  # _positions在基类买卖函数里面被赋值
                self.do_close(pos)
            else:
                self.do_open(pos)

    # 1.follow stop 2.market state change

    def do_close(self, pos):  # 进行平仓
        # next_open = data[self.period]['open'].iloc[pos + 1]
        up_or_down, rate = self.calc_indicator(pos)
        self._lastHighPrice = np.maximum(self._lastHighPrice, self.high.iloc[pos])
        self._lastLowPrice = np.minimum(self._lastLowPrice, self.low.iloc[pos])

        stop_lose_buy = (self._lastHighPrice - self.close.iloc[pos]) > (
            self.params['follow_stop'] * self.close.iloc[pos])
        stop_lose_sell = (self.close.iloc[pos] - self._lastLowPrice) > (
            self.params['follow_stop'] * self.close.iloc[pos])

        close_sell = (self.marketPostion > 0) & (stop_lose_buy | Series(up_or_down < 0, stop_lose_buy.index))
        close_buy = (self.marketPostion < 0) & (stop_lose_sell | Series(up_or_down > 0, stop_lose_buy.index))
        if sum(close_sell) > 0:
            exitPrice = self.open[pos]
            close_vol = np.abs(self.marketPostion)
            self.sell(close_vol, exitPrice)
        if sum(close_buy) > 0:
            exitPrice = self.open[pos]
            close_vol = np.abs(self.marketPostion)
            self.buy_to_cover(close_vol, exitPrice)

    @clockdeco
    def do_open(self, pos):  # 进行开仓
        # next_open = self.next_open(pos)
        # data[self.period]['open'].iloc[pos+1]
        up_or_down, rate = self.calc_indicator(pos)  # 调用方向判断
        if up_or_down == 0:  # 无方向设定则返回
            return
        money = self.params['money']
        if up_or_down == 1:
            location = rate == np.max(rate)  # 定位收益率向量的极值
            open_price = self.open[pos]
            open_vol = pd.to_numeric(money / (open_price * contact.Unit() * contact.Margin()))
            self._lastHighPrice = open_price
            self._lastLowPrice = open_price
            self.buy(open_vol, open_price, location)
        elif up_or_down == -1:
            location = rate == np.min(rate)  # 定位收益率向量的极值
            open_price = self.open[pos]
            open_vol = pd.to_numeric(money / (open_price * contact.Unit() * contact.Margin()))
            self._lastHighPrice = open_price
            self._lastLowPrice = open_price
            self.sell_short(open_vol, open_price, location)

    @clockdeco
    def calc_indicator(self, pos):  # 品种对比统计强弱度

        rate = self.diff[pos]  # 计算收益率,修改后时间从0.002变成0

        rise = rate > 0  # 逻辑变量构造
        fall = rate < 0  # 逻辑变量构造
        tot_len = len(rate)
        nan_len = sum(np.isnan(rate))
        # nan_len = len(rate[np.isnan(rate)])
        valid_len = tot_len - nan_len
        rise_len = sum(rise)
        fall_len = sum(fall)
        up_or_down = 0
        majority_rate = self.params['majority_rate']
        if rise_len > valid_len * majority_rate:  # 交易方向设定
            up_or_down = 1
        elif fall_len > valid_len * majority_rate:
            up_or_down = -1

            # if up_or_down == 0:
            #     print 'hi hello'
        return up_or_down, rate

