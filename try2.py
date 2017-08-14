# encoding: UTF-8

from order import *

from data import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from analysis import *
import math, sys


class IStrategy(object):  # 策略基类，完成基础变量申明、基本方法申明、将来应该把分析部分的方法独立封装


    def __init__(self):
        self._length = 0
        self._orders = {}
        self._seq_orders = []
        self._positions_mt = Series(np.nan, index=g_data['min15']['close'].iloc[0].index)  # 初始化持仓序列
        self._position_price_mt = Series(np.nan, index=g_data['min15']['close'].iloc[0].index)  # 初始化开仓价序列
        self._tradeLog = {}
        self._deals = []
        self._cur_pos = 0
        self._datetime = []
        self._instruments = []
        self._params = {}

    def init_params(self):
        pass  # 由子类实现

    def init(self, instruments, dates=[]):
        self._instruments = instruments  # 交易标的列表
        self._datetime = dates
        self._length = len(dates)
        self.init_params()  # 策略参数
        for instrument in instruments:
            self._orders[instrument] = []  # 委托列表初始化

    # bug 四价未初始化
    def __str__(self):
        pass

    @clockdeco
    def __getattr__(self, name):  # 动态生成数据
        cls = type(self)
        cls.dataKeys = self._dataKeys
        if name in self.dataKeys:
            return eval('self._data[self.period][name]')
        msg = '{.__name__!r} object has no attribute {!r}'
        raise AttributeError(msg.format(cls, name))

    @clockdeco
    def __setattr__(self, name, value):
        cls = type(self)
        dataKeys = g_data[periods[0]].keys()
        # 将关键策略关键字设为只读属性
        if name.lower() in dataKeys:
            error = 'readonly attribute {attr_name!r}'
        elif name.upper() in dataKeys:
            error = "can't set attributes similar to  in {attr_name.lower!r}"
        else:
            error = ''

        if error:
            msg = error.format(cls_name=cls.__name__, attr_name=name)
            raise AttributeError(msg)
        return object.__setattr__(self, name, value)

    #
    # def __getattr__(self, name):
    #     try:
    #         return object.__getattribute__(name)
    #     except:
    #         return name + ' is not found!'
    # def __setattr__(self, key, value):
    #     return  object.__setattr__(self, key, value)
    import numpy as np

    a = [1, 2, 3, 4, 5, -1, -2, -3, -4, -5]
    b = [1, 0, -3, 2, 6, -1, 0, 3, -2, -6]
    a = np.array(a)
    b = np.array(b)
    diff = b - a  # array([ 0, -2, -6, -2,  1,  0,  2,  6,  2, -1])

    location = diff <> 0  # array([False,  True,  True,  True,  True, False,  True,  True,  True,  True], dtype=bool)

    holdExit = np.zeros((1, len(a)))[0]

    holdExit[b==0]= a[b==0]


    def process(self):
        for pos in range(0, self._length):  # 时间轴遍历
            self._cur_pos = pos
            self.loop(pos)
            # self.clear_position()
            self.update_position_martrix()  # 刷新持仓矩阵

    def loop(self, pos):
        pass  # 由子类实现

    def update_position_martrix(self):  # 刷新持仓
        self._positions_mt[(self._positions_mt > 0) | (self._positions_mt < 0)] = np.nan
        self._position_price_mt[self._position_price_mt > 0] = np.nan
        for inst in self._tradeLog:  # self._tradeLog 字典在买卖函数中依据品种分别赋值
            if self._tradeLog[inst]._position != 0:
                self._positions_mt[inst] = self._tradeLog[inst]._position
                self._position_price_mt[inst] = self._tradeLog[inst]._price

    @clockdeco
    def buy(self, vol, price, *condition):
        if len(condition) == 0:
            [self.buy_imp(inst, vol[inst], price[inst]) for inst in price.index]
        else:
            if isinstance(condition[0], bool):  # 规避传入条件是单值的情况
                condition = dict([condition[0]] * len(price.index), price.index)
            [self.buy_imp(inst, vol[inst], price[inst]) for inst in price.index if condition[0][inst] == True]

    @clockdeco
    def sell_short(self, vol, price, *condition):
        if len(condition) == 0:
            [self.sell_short_imp(inst, vol[inst], price[inst]) for inst in price.index]
        else:
            if isinstance(condition[0], bool):  # 规避传入条件是单值的情况
                condition = dict([condition[0]] * len(price.index), price.index)
            [self.sell_short_imp(inst, vol[inst], price[inst]) for inst in price.index if condition[0][inst] == True]

    @clockdeco
    def sell(self, vol, price, *condition):

        if len(condition) == 0:
            [self.sell_imp(inst, vol[inst], price[inst]) for inst in price.index]
        else:
            if isinstance(condition[0], bool):  # 规避传入条件是单值的情况
                condition = dict([condition[0]] * len(price.index), price.index)
            [self.sell_imp(inst, vol[inst], price[inst]) for inst in price.index if condition[0][inst] == True]

    @clockdeco
    def buy_to_cover(self, vol, price, *condition):  # vol手数
        if len(condition) == 0:
            [self.buy_to_cover_imp(inst, vol[inst], price[inst]) for inst in price.index]
        else:
            if isinstance(condition[0], bool):  # 规避传入条件是单值的情况
                condition = dict([condition[0]] * len(price.index), price.index)
            [self.buy_to_cover_imp(inst, vol[inst], price[inst]) for inst in price.index if condition[0][inst] == True]

    def buy_imp(self, instrument, vol, price):
        vol = math.floor(vol)
        if vol <= 0 or math.isnan(price) or math.isnan(vol):
            return
        time = self._datetime[self._cur_pos]
        order = Order(instrument, trade_enum.Buy, trade_enum.Entry, price, vol, time)
        self._orders[instrument].append(order)
        self._seq_orders.append(order)
        if self._tradeLog.has_key(instrument):  # 对应品种已有持仓
            ins_position = self._tradeLog.get(instrument)
            ins_position._position += vol  # 加仓
            ins_position._price = abs(
                (ins_position._price * ins_position._position + price * vol) / (ins_position._position + vol))  #
        else:
            self._tradeLog[instrument] = Position(vol, price)  # 记录对应品种持仓

    def sell_imp(self, instrument, vol, price):
        if vol <= 0 or math.isnan(price) or math.isnan(vol):
            return
        time = self._datetime[self._cur_pos]
        ins_position = None
        position = 0
        if self._tradeLog.has_key(instrument):
            ins_position = self._tradeLog.get(instrument)
            position = ins_position._position
        else:
            print 'Error nothing to sell %s' % instrument
            return
        order = None
        if vol == 0 and position > 0:
            order = Order(instrument, trade_enum.Sell, trade_enum.Exit, price, position,
                          time)  # 构造委托记录以便追加到self._orders
            del (self._tradeLog[instrument])
        elif position > 0:
            order = Order(instrument, trade_enum.Sell, trade_enum.Exit, price, min(vol, position),
                          time)  # 构造委托记录以便追加到self._orders
            if vol >= position:
                del (self._tradeLog[instrument])
            else:
                ins_position._position = position - vol
        elif position <= 0:
            if position == 0:
                del (self._tradeLog[instrument])
            print 'Error nothing to sell %s' % instrument
        if order is not None:
            # self._orders[instrument].append(order)
            self._seq_orders.append(order)

    def sell_short_imp(self, instrument, vol, price):  # 针对品种进行交易
        global g_sell, g_open
        vol = math.floor(vol)
        if vol <= 0 or math.isnan(price) or math.isnan(vol):
            return
        time = self._datetime[self._cur_pos]
        order = Order(instrument, trade_enum.Sell, trade_enum.Entry, price, vol, time)
        self._orders[instrument].append(order)  # 对委托记录进行追加
        self._seq_orders.append(order)
        if self._tradeLog.has_key(instrument):  # 对应品种有记录则追加
            ins_position = self._tradeLog.get(instrument)
            ins_position._position -= vol
            ins_position._price = abs(
                (ins_position._price * ins_position._position - price * vol) \
                / (ins_position._position - vol)
            )
        else:  # 否则新建记录
            # position = Position(-vol, price)
            self._tradeLog[instrument] = Position(-vol, price)

    def buy_to_cover_imp(self, instrument, vol, price):
        global g_buy, g_close
        if vol <= 0 or math.isnan(price) or math.isnan(vol):
            return
        time = self._datetime[self._cur_pos]
        ins_position = None
        position = 0
        if self._tradeLog.has_key(instrument):
            ins_position = self._tradeLog.get(instrument)  # 取得品种对应持仓信息
            position = ins_position._position  # 取品种仓位
        else:
            print 'Error nothing to buy_to_cover_imp %s' % instrument
            return
        order = None
        if vol == 0 and position < 0:
            order = Order(instrument, trade_enum.Buy, trade_enum.Exit, price, abs(position), time)
            del (self._tradeLog[instrument])
        elif position < 0:
            order = Order(instrument, trade_enum.Buy, trade_enum.Exit, price, min(vol, abs(position)), time)
            if vol >= abs(position):
                del (self._tradeLog[instrument])
            else:
                ins_position._position = abs(position + vol)
        elif position >= 0:
            if position == 0:
                del (self._tradeLog[instrument])
            print 'Error nothing to buyToCover %s' % instrument
        if order is not None:
            # self._orders[instrument].append(order)
            self._seq_orders.append(order)

    # 固定关键变量为只读属性,只读控制由元类object继承
    # @property
    # def high(self):
    #     return self._high
    #
    # @property
    # def open(self):
    #     return self._open
    #
    # @property
    # def low(self):
    #     return self._low
    #
    # @property
    # def close(self):
    #     return self._close
    #
    # @property
    # def vol(self):
    #     return self._vol
    #
    # @property
    # def opi(self):
    #     return self._opi
    @property
    def marketPostion(self):  # 调用持仓量为只读属性，且内部返回self._positions_mt矩阵
        return self._positions_mt

    @property
    def entryPrice(self):  # 调用入场价为只读属性，且内部返回self._positions_mt矩阵
        return self._position_price_mt

    @property
    def params(self):
        return self._params

    # by instrument
    # def statistics(self):
    #     global g_product_info, g_fee, g_min_tick, g_unit, g_buy, g_sell, g_open, g_close
    #     totpnl = 0
    #     for instrument in self._instruments:
    #
    #         position = 0
    #         avg_EntryPrice = 0
    #         pnl = 0
    #         close_pnl = 0
    #         for order in self._orders[instrument]:
    #             if order._direction == g_buy and order._offset == g_open:
    #                 avg_EntryPrice = (avg_EntryPrice * position + order._price * order._vol) / (position + order._vol)
    #                 position += order._vol
    #             elif order._direction == g_sell and order._offset == g_open:
    #                 avg_EntryPrice = (avg_EntryPrice * position - order._price * order._vol) / (position - order._vol)
    #                 position -= order._vol
    #             elif order._direction == g_buy and order._offset == g_close:
    #                 close_pnl = (avg_EntryPrice - order._price) * order._vol
    #                 pnl += close_pnl
    #                 if order._vol == abs(position):
    #                     avg_EntryPrice = 0
    #                     position = 0
    #                 else:
    #                     avg_EntryPrice = (avg_EntryPrice * position + order._price * order._vol) / (
    #                         position + order._vol)
    #                     position += order._vol
    #             elif order._direction == g_sell and order._offset == g_close:
    #                 close_pnl = (order._price - avg_EntryPrice) * order._vol
    #                 pnl += close_pnl
    #                 if order._vol == position:
    #                     avg_EntryPrice = 0
    #                     position = 0
    #                 else:
    #                     avg_EntryPrice = (avg_EntryPrice * position - order._price * order._vol) / (
    #                         position - order._vol)
    #                     position -= order._vol
    #             print order, close_pnl, pnl
    #         totpnl += pnl * g_product_info[instrument][1]
    #     print totpnl

    # by order sequence
    def seq_statistics(self):
        global g_product_info, g_fee, g_min_tick, g_unit, g_buy, g_sell, g_open, g_close
        totpnl = 0
        insts_info = {}
        for instrument in self._instruments:
            insts_info[instrument] = {'position': 0, 'avg_EntryPrice': 0,
                                      'pnl': 0, 'close_pnl': 0}

        for order in self._seq_orders:  # 逐笔计算盈亏数据
            inst_fee = contact.Fee()[order._instrument]  # 手续费
            inst_slip = contact.MinTick()[order._instrument] * contact.Unit()[order._instrument]  # 滑点

            position = insts_info[order._instrument]['position']  # 持仓
            avg_EntryPrice = insts_info[order._instrument]['avg_EntryPrice']  # 持仓均价
            pnl = insts_info[order._instrument]['pnl']  # 该合约目前的总盈亏
            close_pnl = 0  # 平仓盈亏

            if order._direction == trade_enum.Buy and order._offset == trade_enum.Entry:  # 多开
                # 更新持仓均价
                avg_EntryPrice = (avg_EntryPrice * position + order._price * order._vol) / (position + order._vol)
                # 更新持仓
                position += order._vol
            elif order._direction == trade_enum.Sell and order._offset == trade_enum.Exit:  # 空开
                avg_EntryPrice = (avg_EntryPrice * position - order._price * order._vol) / (position - order._vol)
                position -= order._vol
            elif order._direction == trade_enum.Buy and order._offset == trade_enum.Exit:  # 空平
                if order._price == 0 or avg_EntryPrice == 0:  # 这是特殊情况，发生一般是说明next_open没有取到(比如最后一根K线)
                    close_pnl = 0
                else:
                    close_pnl = (avg_EntryPrice - order._price) * order._vol  # 计算该笔平仓的平仓盈亏
                pnl += close_pnl  # 更新该合约总的盈亏
                if order._vol == abs(position):
                    avg_EntryPrice = 0
                    position = 0
                else:
                    avg_EntryPrice = (avg_EntryPrice * position + order._price * order._vol) / (
                        position + order._vol)
                    position += order._vol
            elif order._direction == trade_enum.Sell and order._offset == trade_enum.Exit:  # 多平
                if order._price == 0 or avg_EntryPrice == 0:
                    close_pnl = 0
                else:
                    if order._price == 0 or avg_EntryPrice == 0:
                        close_pnl = 0
                    else:
                        close_pnl = (order._price - avg_EntryPrice) * order._vol
                pnl += close_pnl
                if order._vol == position:
                    avg_EntryPrice = 0
                    position = 0
                else:
                    avg_EntryPrice = (avg_EntryPrice * position - order._price * order._vol) / (
                        position - order._vol)
                    position -= order._vol
            insts_info[order._instrument]['position'] = position  # 更新该合约的持仓
            insts_info[order._instrument]['avg_EntryPrice'] = avg_EntryPrice  # 更新该合约的持仓均价
            insts_info[order._instrument]['pnl'] = pnl  # 更新该合约的总盈亏
            insts_info[order._instrument]['close_pnl'] = close_pnl  # 更新该合约的最后一笔交易平仓盈亏

            totpnl += close_pnl * g_product_info[order._instrument][g_unit] - inst_fee - inst_slip  # 更新所有合约的总平仓盈亏

            # 最后赋值委托中的变量 ，最后画图需要用到每笔委托的这些值
            order._close_pnl = close_pnl  # 更新对应品种交易的累计盈亏
            order._instrument_pnl = pnl  # 更新对应品种的平仓盈亏
            order._tot_pnl = totpnl  # 更新所有品种的累计盈亏

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
