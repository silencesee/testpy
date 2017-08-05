# encoding: UTF-8

from data import *


class Order(object):
    def __init__(self, instrument, dir, offset, price, vol, time):
        self._instrument = instrument
        self._direction = dir
        self._offset = offset
        self._price = price
        self._vol = vol
        self._time = time
        self._close_pnl = 0
        self._instrument_pnl = 0
        self._tot_pnl = 0

    def __str__(self):
        return '%s, %s, %s, %s, price: %lf, vol: %d' % (
            self._instrument, self._time, g_DirectionType[self._direction], g_OffsetType[self._offset], self._price,
            self._vol)
