# encoding: UTF-8
from __future__ import division  # 正常除法，此导入必须置顶优先，否则报错
from globalVars import *
import matplotlib.pyplot as plt
import copy, math
import pandas as pd


def clockdeco(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
            arg_lst.append(', '.join(pairs))

        print('函数 %s  耗时 [%0.8fs]' % (name, elapsed))
        # print ('参数 %s' %(', '.join(arg_lst)))
        # print ('运行结果%r' %(result))
        # print ('耗时 [%0.8fs] '% (elapsed))
        return result

    return clocked


class Statistics(object):
    def __init__(self, tradeLog):
        self.record = tradeLog
        start = tradeLog.tradeNum + 1
        end = len(tradeLog.holdingPrice) + 1
        cut = range(start, end)
        self.holdingPrice = np.delete(tradeLog.holdingPrice, cut, 0)
        self.exitPrice = np.delete(tradeLog.exitPrice, cut, 0)
        self.holdingLots = np.delete(tradeLog.holdingLots, cut, 0)
        self.exitLots = np.delete(tradeLog.exitLots, cut, 0)
        self._recorder.time[self._tradeNum] = self._curTime = tradeLog.time
        self.eventTimes = tradeLog.tradeNum

    def netprofit(self):

        location = np.array(map(lambda x: x.any(), self.exitPrice[:]))
        location1 = copy.copy(location)
        location1[0:-1] = location[1:]
        location1[-1] = location[0]
        # 平仓盈亏点数*平仓手数*每手
        result = (self.exitPrice[location] - self.holdingPrice[location1]) * self.exitLots[location] * contact.unit
        netprofit = result.sum(axis=1)
        self.time = self.time[location]


        return netprofit

    def netprofit_single(self, inst):
        if inst is str:

            clocation = instruments.index(inst)
        else:
            clocation = inst
        location = np.array(map(lambda x: x.any(), self.exitPrice[:, clocation]))
        location1 = copy.copy(location)
        location1[0:-1] = location[1:]
        location1[-1] = location[0]
        result = (self.exitPrice[location, clocation] - self.holdingPrice[location1, clocation]) * self.exitLots[location, clocation] * contact.unit[clocation]
        netprofit = result[:, clocation]
        self.time = self.time[location]


        #  规避某些品种可能还没有上市的空值
        location = self.exitPrice[location, clocation] <> 0
        b = np.where(location == 1)[0]
        return netprofit

    # 绘图模块
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

    def calc_sharp(self):  # 夏普率
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
