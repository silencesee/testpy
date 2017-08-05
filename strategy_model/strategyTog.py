# encoding: UTF-8

from strategy import IStrategy
from data import *
import math
import numpy as np
import pandas as pd


class StrategyTog(IStrategy):  # 策略实例，继承自策略基类

    def __init__(self, period):
        IStrategy.__init__(self)
        self._period = period
        self._lastHighPrice = {}
        self._lastLowPrice = {}

    def __str__(self):
        pass

    @property
    def period(self):
        return self._period

    def init_params(self):
        self._params['follow_stop'] = 0.01
        self._params['nan_rate'] = 0.4
        self._params['majority_rate'] = 0.9  # 设置全市场共振阀值
        self._params['money'] = 100000

    # 1.follow stop 2.market state change
    def do_close(self, pos):  # 进行平仓
        global g_data
        high = g_data[self.period]['high']
        low = g_data[self.period]['low']
        close = g_data[self.period]['close']

        # next_open = data[self.period]['open'].iloc[pos + 1]

        up_or_down, rate = self.calc_indicator(pos)

        self._lastHighPrice = np.maximum(self._lastHighPrice, high.iloc[pos])
        self._lastLowPrice = np.minimum(self._lastLowPrice, low.iloc[pos])

        stop_lose_buy = (self._lastHighPrice - close.iloc[pos]) > (self._params['follow_stop'] * close.iloc[pos])
        stop_lose_sell = (close.iloc[pos] - self._lastLowPrice) > (self._params['follow_stop'] * close.iloc[pos])

        close_sell = (self._positions_mt > 0) & (stop_lose_buy | Series(up_or_down < 0, stop_lose_buy.index))
        close_buy = (self._positions_mt < 0) & (stop_lose_sell | Series(up_or_down > 0, stop_lose_buy.index))
        if sum(close_sell) > 0:
            close_price = self.next_open(pos, close_sell)
            close_vol = np.abs(self._positions_mt)
            self.sell(close_vol, close_price)
        if sum(close_buy) > 0:
            close_price = self.next_open(pos, close_buy)
            close_vol = np.abs(self._positions_mt)
            self.buy_to_cover(close_vol, close_price)

    def calc_indicator(self, pos):  # 品种对比统计强弱度
        global g_data
        close = g_data[self.period]['close']  # 取收盘价
        rate = (close.iloc[pos] - close.iloc[pos - 1]) / close.iloc[pos - 1]  # 计算收益率
        rise = rate > 0  # 逻辑变量构造
        fall = rate < 0  # 逻辑变量构造
        tot_len = len(rate)
        nan_len = sum(np.isnan(rate))
        # nan_len = len(rate[np.isnan(rate)])
        valid_len = tot_len - nan_len
        rise_len = sum(rise)
        fall_len = sum(fall)
        up_or_down = 0
        majority_rate = self._params['majority_rate']
        if rise_len > valid_len * majority_rate:  # 交易方向设定
            up_or_down = 1
        elif fall_len > valid_len * majority_rate:
            up_or_down = -1

            # if up_or_down == 0:
            #     print 'hi hello'
        return up_or_down, rate

    def do_open(self, pos):  # 进行开仓
        # next_open = self.next_open(pos)
        # data[self.period]['open'].iloc[pos+1]
        up_or_down, rate = self.calc_indicator(pos)  # 调用方向判断
        if up_or_down == 0:  # 无方向设定则返回
            return
        money = self._params['money']
        if up_or_down == 1:
            open_price = self.next_open(pos, rate == np.max(rate))
            open_vol = pd.to_numeric(money / (g_products.loc['unit'] * open_price * g_products.loc['margin']))
            self._lastHighPrice = open_price
            self._lastLowPrice = open_price
            self.buy(open_vol, open_price)
        elif up_or_down == -1:
            open_price = self.next_open(pos, rate == np.min(rate))
            open_vol = pd.to_numeric(money / (g_products.loc['unit'] * open_price * g_products.loc['margin']))
            self._lastHighPrice = open_price
            self._lastLowPrice = open_price
            self.sell_short(open_vol, open_price)

    def loop(self, pos):
        if len(self._positions) > 0:
            self.do_close(pos)
        else:
            self.do_open(pos)

    def next_open(self, pos, condition):  # 空值预判
        global g_data
        open = g_data[self.period]['open']
        count = pos + 1

        if count >= self._length:
            return 0
        nextopen = open.iloc[count][condition]

        while count < self._length and sum(np.isnan(nextopen)) != 0:
            nextopen[np.isnan(open.iloc[count][condition]) == False] = open.iloc[count]
            count += 1

        # 这里如果越界取了最后的open，其实应该取close更合理，但是一根k线对整体的回测影响不大

        pos_last = min(count, self._length - 1)
        nextopen[np.isnan(nextopen)] = open.iloc[pos_last]
        nextopen = nextopen.reindex(open.iloc[pos_last].index)
        return nextopen
