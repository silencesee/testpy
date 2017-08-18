# encoding: UTF-8

from strategy_model import *
from analysis import *
from timeit import timeit
np.seterr(invalid='ignore')  # 忽略nan比较时的警告


class Strategy_Inst(Strategy_model):  # 策略实例，继承自策略基类
    def __init__(self, timelist, dataKeys):  # 策略运行参数
        super(Strategy_Inst, self).__init__(timelist, dataKeys)  # 调用父类方法

    def int_params(self):  # 策略逻辑参数,可以在这里初始化一些循环体外的变量或者方法
        self._params['follow_stop'] = 0.01
        self._params['nan_rate'] = 0.4
        self._params['majority_rate'] = 0.9  # 设置全市场共振阀值

    def int_vars(self):  # 序列变量申明段类似于TB里面的series
        size = np.shape(self.close)
        self.rate = np.zeros(size)
        pass

    # @clockdeco
    def strategy_body(self, pos):  # 具体策略主体
        if pos > 2:

            direct, rate = self.calc_indicator(pos)

            lots = floor(money / (contact.unit * self.open[pos] * contact.margin))

            if direct > 0:
                maxrate, location = findmax(rate)  # 求收益率极值
                self.order(lots, self.open[pos], location)
            elif direct < 0:
                minrate, location = findmin(rate)  # 求收益率极值
                self.order(-1 * lots, self.open[pos], location)
                # print pos
                # print self.open[pos]


    # @clockdeco
    def calc_indicator(self, pos):  # 策略内部实现的算法品种对比统计强弱度
        # a = time.time()
        rate = (np.array(self.close[pos - 1]) - np.array(self.close[pos - 2])) / np.array(self.close[pos - 2])  # 计算收益率

        # print (str(pos) +'耗时 [%0.8fs] ' % (time.time()-a))
        rise = rate > 0  # 逻辑变量构造
        fall = rate < 0  # 逻辑变量构造
        tot_len = len(rate)  # 当前时刻总交易品种
        nan_len = sum(np.isnan(rate))  # 当前时刻不可交易的品种
        # nan_len = len(rate[np.isnan(rate)])
        valid_len = tot_len - nan_len  # 当前时刻可以交易的品种数目
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
