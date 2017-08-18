# encoding: UTF-8
from __future__ import division  # 正常除法，此导入必须置顶优先，否则报错
from globalVars import *
import matplotlib.pyplot as plt
import copy, functools, time
import pandas as pd
from config import *


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
        # 截取有效交易记录
        self.holdingPrice = np.delete(tradeLog.holdingPrice, cut, 0)
        self.exitPrice = np.delete(tradeLog.exitPrice, cut, 0)
        self.holdingLots = np.delete(tradeLog.holdingLots, cut, 0)
        self.exitLots = np.delete(tradeLog.exitLots, cut, 0)
        self.traded = np.delete(tradeLog.traded, cut, 0)
        self.time = np.delete(tradeLog.time, cut, 0)
        self.eventTimes = tradeLog.tradeNum

    def netprofit(self):
        if len(instruments) > 1:  # 若初始计算品种只有一个则跳转到单品种计算模式

            location = np.array(map(lambda x: x.any(), self.exitPrice[:]))  # 平仓动作定位
            location1 = copy.copy(location)
            location1[0:-1] = location[1:]
            location1[-1] = location[0]  # 构造上一笔开仓信息的定位点
            # 平仓盈亏点数*平仓手数*每手
            result = (self.exitPrice[location] - self.holdingPrice[location1]) * self.exitLots[
                location] * contact.unit * self.traded[location].astype(int)
            cost = (self.exitPrice[location] + self.holdingPrice[location1]) * np.abs(
                self.exitLots[location]) * contact.unit * \
                   self.traded[location].astype(int) * costRate
            result += cost
            profit = result.sum(axis=1)  # 每个品种横向相加，再纵向累加
            timeindex = self.time[location]

            netprofit = pd.Series(profit.cumsum(), index=timeindex)
            plt.figure(figsize=(8, 4))
            plt.plot(netprofit, label="$captial$", color="red", linewidth=2)
            plt.xlabel("time")
            plt.ylabel("netprofit")
            # plt.title("累计平仓盈亏")

            plt.legend()
            plt.show()
            return netprofit
        else:
            self.netprofit_single(1)

    def netprofit_single(self, inst):
        if type(inst) is str:

            clocation = instruments.index(inst)
        else:
            clocation = inst
        location = np.array(map(lambda x: x.any(), self.exitPrice[:, clocation]))
        location1 = copy.copy(location)
        location1[0:-1] = location[1:]
        location1[-1] = location[0]
        result = (self.exitPrice[location, clocation] - self.holdingPrice[location1, clocation]) * self.exitLots[
            location, clocation] * contact.unit[clocation] * self.traded[location, clocation].astype(
            int)  # 获取对应品种的交易记录，并计算盈亏
        cost = (self.exitPrice[location, clocation] + self.holdingPrice[location1, clocation]) * np.abs(self.exitLots[
                                                                                                            location, clocation]) * \
               contact.unit[clocation] * self.traded[location, clocation].astype(
            int) * costRate * 2
        result += cost
        netprofit = result.cumsum()
        timeindex = self.time[location]
        netprofit = pd.Series(netprofit, index=timeindex)
        # self.time = self.time[location]  # 获取对应品种的交易事件发生时间
        plt.figure(figsize=(8, 4))
        plt.plot(netprofit, label="$captial$", color="red", linewidth=2)
        plt.xlabel("time")
        plt.ylabel("netprofit")
        #  规避某些品种可能还没有上市的空值
        location = self.exitPrice[location, clocation] <> 0
        b = np.where(location == 1)[0]
        return netprofit


        # def calc_sharp(self):  # 夏普率
        #     times = [order._time for order in self._seq_orders]
        #     capital = [order._tot_pnl for order in self._seq_orders]
        #     data1 = pd.DataFrame({'time': times, 'capital': capital}, index=times)
        #     data2 = data1.reindex(self._datetime, method='ffill')
        #     data3 = data2.resample('D').last()
        #     data4 = data3.dropna()
        #     tmp = data4.capital
        #     N = len(tmp)
        #
        #     values = []
        #     for i in range(1, N):
        #         values.append(tmp[i] - tmp[i - 1])
        #
        #     values = pd.Series(values)
        #
        #     dev = values.std()
        #     mean = values.mean()
        #     sharp = math.sqrt(250) * mean / dev
        #
        #     return sharp
