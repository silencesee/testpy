# encoding: UTF-8

from order import Order
from position import Position
from data import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math


class IStrategy(object):  # 策略基类，完成基础变量申明、基本方法申明、将来应该把分析部分的方法独立封装


    def __init__(self):
        self._length = 0
        self._orders = {}
        self._seq_orders = []
        self._positions_mt = Series(np.nan, index=g_data['min15']['close'].iloc[0].index)  # 初始化持仓序列
        self._position_price_mt = Series(np.nan, index=g_data['min15']['close'].iloc[0].index)  # 初始化开仓价序列
        self._positions = {}
        self._deals = []
        self._cur_pos = 0
        self._datetime = []
        self._instruments = []
        self._params = {}

    def __str__(self):
        pass

    def loop(self, pos):
        pass  # 由子类实现

    def init_params(self):
        pass  # 由子类实现

    def init(self, instruments, dates=[]):
        self._instruments = instruments  # 交易标的列表
        self._datetime = dates
        self._length = len(dates)
        self.init_params()  # 策略参数
        for instrument in instruments:
            self._orders[instrument] = []  # 委托列表初始化

    def process(self):
        for pos in range(0, self._length):  # 时间轴遍历
            self._cur_pos = pos
            self.loop(pos)
            # self.clear_position()
            self.update_position_martrix()  # 刷新持仓矩阵

    def buy(self, vol, price):
        [self.buy_imp(inst, vol[inst], price[inst]) for inst in price.index]

    def sell_short(self, vol, price):
        [self.sell_short_imp(inst, vol[inst], price[inst]) for inst in price.index]

    def sell(self, vol, price):
        [self.sell_imp(inst, vol[inst], price[inst]) for inst in price.index]

    def buy_to_cover(self, vol, price):  # vol手数
        [self.buy_to_cover_imp(inst, vol[inst], price[inst]) for inst in price.index]

    def update_position_martrix(self):  # 刷新持仓
        self._positions_mt[(self._positions_mt > 0) | (self._positions_mt < 0)] = np.nan
        self._position_price_mt[self._position_price_mt > 0] = np.nan
        for inst in self._positions:
            if self._positions[inst]._position != 0:
                self._positions_mt[inst] = self._positions[inst]._position
                self._position_price_mt[inst] = self._positions[inst]._price

    def buy_imp(self, instrument, vol, price):
        global g_buy, g_open
        vol = math.floor(vol)
        if vol <= 0 or math.isnan(price) or math.isnan(vol):
            return
        time = self._datetime[self._cur_pos]
        order = Order(instrument, g_buy, g_open, price, vol, time)
        self._orders[instrument].append(order)
        self._seq_orders.append(order)
        if self._positions.has_key(instrument):  # 对应品种已有持仓
            ins_position = self._positions.get(instrument)
            ins_position._position += vol  # 加仓
            ins_position._price = abs(
                (ins_position._price * ins_position._position + price * vol)
                / (ins_position._position + vol)
            )  #
        else:
            self._positions[instrument] = Position(vol, price)  # 记录对应品种持仓

    def sell_imp(self, instrument, vol, price):
        global g_sell, g_close
        if vol <= 0 or math.isnan(price) or math.isnan(vol):
            return
        time = self._datetime[self._cur_pos]
        ins_position = None
        position = 0
        if self._positions.has_key(instrument):
            ins_position = self._positions.get(instrument)
            position = ins_position._position
        else:
            print 'Error nothing to sell %s' % instrument
            return
        order = None
        if vol == 0 and position > 0:
            order = Order(instrument, g_sell, g_close, price, position, time)  # 构造委托记录以便追加到self._orders
            del (self._positions[instrument])
        elif position > 0:
            order = Order(instrument, g_sell, g_close, price, min(vol, position), time)  # 构造委托记录以便追加到self._orders
            if vol >= position:
                del (self._positions[instrument])
            else:
                ins_position._position = position - vol
        elif position <= 0:
            if position == 0:
                del (self._positions[instrument])
            print 'Error nothing to sell %s' % instrument
        if order is not None:
            self._orders[instrument].append(order)
            self._seq_orders.append(order)

    def sell_short_imp(self, instrument, vol, price):  # 针对品种进行交易
        global g_sell, g_open
        vol = math.floor(vol)
        if vol <= 0 or math.isnan(price) or math.isnan(vol):
            return
        time = self._datetime[self._cur_pos]
        order = Order(instrument, g_sell, g_open, price, vol, time)
        self._orders[instrument].append(order)  # 对委托记录进行追加
        self._seq_orders.append(order)
        if self._positions.has_key(instrument):
            ins_position = self._positions.get(instrument)
            ins_position._position -= vol
            ins_position._price = abs(
                (ins_position._price * ins_position._position - price * vol) \
                / (ins_position._position - vol)
            )
        else:
            # position = Position(-vol, price)
            self._positions[instrument] = Position(-vol, price)

    def buy_to_cover_imp(self, instrument, vol, price):
        global g_buy, g_close
        if vol <= 0 or math.isnan(price) or math.isnan(vol):
            return
        time = self._datetime[self._cur_pos]
        ins_position = None
        position = 0
        if self._positions.has_key(instrument):
            ins_position = self._positions.get(instrument)
            position = ins_position._position
        else:
            print 'Error nothing to buy_to_cover_imp %s' % instrument
            return
        order = None
        if vol == 0 and position < 0:
            order = Order(instrument, g_buy, g_close, price, abs(position), time)
            del (self._positions[instrument])
        elif position < 0:
            order = Order(instrument, g_buy, g_close, price, min(vol, abs(position)), time)
            if vol >= abs(position):
                del (self._positions[instrument])
            else:
                ins_position._position = abs(position + vol)
        elif position >= 0:
            if position == 0:
                del (self._positions[instrument])
            print 'Error nothing to buyToCover %s' % instrument
        if order is not None:
            self._orders[instrument].append(order)
            self._seq_orders.append(order)

    # by instrument
    def statistics(self):
        global g_product_info, g_fee, g_min_tick, g_unit, g_buy, g_sell, g_open, g_close
        totpnl = 0
        for instrument in self._instruments:

            position = 0
            last_open_price = 0
            pnl = 0
            close_pnl = 0
            for order in self._orders[instrument]:
                if order._direction == g_buy and order._offset == g_open:
                    last_open_price = (last_open_price * position + order._price * order._vol) / (position + order._vol)
                    position += order._vol
                elif order._direction == g_sell and order._offset == g_open:
                    last_open_price = (last_open_price * position - order._price * order._vol) / (position - order._vol)
                    position -= order._vol
                elif order._direction == g_buy and order._offset == g_close:
                    close_pnl = (last_open_price - order._price) * order._vol
                    pnl += close_pnl
                    if order._vol == abs(position):
                        last_open_price = 0
                        position = 0
                    else:
                        last_open_price = (last_open_price * position + order._price * order._vol) / (
                            position + order._vol)
                        position += order._vol
                elif order._direction == g_sell and order._offset == g_close:
                    close_pnl = (order._price - last_open_price) * order._vol
                    pnl += close_pnl
                    if order._vol == position:
                        last_open_price = 0
                        position = 0
                    else:
                        last_open_price = (last_open_price * position - order._price * order._vol) / (
                            position - order._vol)
                        position -= order._vol
                print order, close_pnl, pnl
            totpnl += pnl * g_product_info[instrument][1]
        print totpnl

    # by order sequence
    def seq_statistics(self):
        global g_product_info, g_fee, g_min_tick, g_unit, g_buy, g_sell, g_open, g_close
        totpnl = 0
        insts_info = {}
        for instrument in self._instruments:
            insts_info[instrument] = {'position': 0, 'last_open_price': 0,
                                      'pnl': 0, 'close_pnl': 0}

        for order in self._seq_orders:
            inst_fee = g_product_info[order._instrument][g_fee]
            inst_slip = g_product_info[order._instrument][g_min_tick] * g_product_info[order._instrument][g_unit]

            position = insts_info[order._instrument]['position']
            last_open_price = insts_info[order._instrument]['last_open_price']
            pnl = insts_info[order._instrument]['pnl']
            close_pnl = 0

            if order._direction == g_buy and order._offset == g_open:
                last_open_price = (last_open_price * position + order._price * order._vol) / (position + order._vol)
                position += order._vol
            elif order._direction == g_sell and order._offset == g_open:
                last_open_price = (last_open_price * position - order._price * order._vol) / (position - order._vol)
                position -= order._vol
            elif order._direction == g_buy and order._offset == g_close:
                if order._price == 0 or last_open_price == 0:
                    close_pnl = 0
                else:
                    close_pnl = (last_open_price - order._price) * order._vol
                pnl += close_pnl
                if order._vol == abs(position):
                    last_open_price = 0
                    position = 0
                else:
                    last_open_price = (last_open_price * position + order._price * order._vol) / (
                        position + order._vol)
                    position += order._vol
            elif order._direction == g_sell and order._offset == g_close:
                if order._price == 0 or last_open_price == 0:
                    close_pnl = 0
                else:
                    if order._price == 0 or last_open_price == 0:
                        close_pnl = 0
                    else:
                        close_pnl = (order._price - last_open_price) * order._vol
                pnl += close_pnl
                if order._vol == position:
                    last_open_price = 0
                    position = 0
                else:
                    last_open_price = (last_open_price * position - order._price * order._vol) / (
                        position - order._vol)
                    position -= order._vol
            insts_info[order._instrument]['position'] = position
            insts_info[order._instrument]['last_open_price'] = last_open_price
            insts_info[order._instrument]['pnl'] = pnl
            insts_info[order._instrument]['close_pnl'] = close_pnl

            totpnl += close_pnl * g_product_info[order._instrument][g_unit] - inst_fee - inst_slip

            order._close_pnl = close_pnl
            order._instrument_pnl = pnl
            order._tot_pnl = totpnl

            print order, close_pnl, pnl, totpnl

        return self._seq_orders

    def plot_capital(self):
        times = [order._time for order in self._seq_orders]
        capital = [order._tot_pnl for order in self._seq_orders]

        data1 = pd.DataFrame({'time': times, 'capital': capital}, index=times)
        data2 = data1.reindex(self._datetime, method='ffill')
        data3 = data2.resample('D').last()
        data4 = data3.dropna()

        plt.figure(figsize=(8, 4))
        plt.plot(data4.time, data4.capital, label="$captial$", color="red", linewidth=2)

        plt.xlabel("time")
        plt.ylabel("capital")
        plt.title("Capital curve diagram")

        plt.legend()
        plt.show()

    def calc_sharp(self):
        times = [order._time for order in self._seq_orders]
        capital = [order._tot_pnl for order in self._seq_orders]
        data1 = pd.DataFrame({'time': times, 'capital': capital}, index=times)
        data2 = data1.reindex(self._datetime, method='ffill')
        data3 = data2.resample('D').last()
        data4 = data3.dropna()
        tmp = data4.capital
        N = len(tmp)

        values = []
        for i in range(1, N):
            values.append(tmp[i] - tmp[i - 1])

        values = pd.Series(values)

        dev = values.std()
        mean = values.mean()
        sharp = math.sqrt(250) * mean / dev

        return sharp
