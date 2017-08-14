# encoding: UTF-8

from data import *


class Order(object):
    def __init__(self, instrument, buyOrSell, entryOrExit, price, vol, time):  # 类似于A函数的买卖方向和开平方向结构
        self._instrument = instrument
        self._direction = buyOrSell
        self._offset = entryOrExit
        self._price = price
        self._vol = vol
        self._time = time
        self._close_pnl = 0
        self._instrument_pnl = 0
        self._tot_pnl = 0

        # def __str__(self):
        #     return '%s, %s, %s, %s, price: %lf, vol: %d' % (
        #         self._instrument, self._time, g_DirectionType[self._direction], g_OffsetType[self._offset], self._price,
        #         self._vol)


class Position(object):
    def __init__(self, vol, price):
        self._position = vol
        self._price = price
        pass

    def __str__(self):
        pass
