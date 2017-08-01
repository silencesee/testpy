# encoding: UTF-8
from __future__ import division  # 正常除法，此导入必须置顶优先，否则报错
import numpy as np
import scipy
from scipy.optimize import brentq
from scipy.stats import norm
from math import exp, sqrt, log


# spot 当前价
# strike 行权价
# maturity 到期期限
# r 无风险利率
# vol 波动率

# 期权计算的蒙特卡洛方法
def call_option_pricer_monte_carlo(spot, strike, maturity, r, vol, numOfPath=100000):
    randomSeries = scipy.random.randn(numOfPath)
    s_t = spot * np.exp((r - 0.5 * vol * vol) * maturity + randomSeries * vol * sqrt(maturity))
    sumValue = np.maximum(s_t - strike, 0.0).sum()
    price = exp(-r * maturity) * sumValue / numOfPath
    return price


# Black - Scholes 定价公式  变量为原生资产（underlying asset，如股票等）和时间，参数为波动率和利率，均假设为常数。
def call_option_pricer(spot, strike, maturity, r, vol):
    d1 = (log(spot / strike) + (r + 0.5 * vol * vol) * maturity) / vol / sqrt(maturity)
    d2 = d1 - vol * sqrt(maturity)

    price = spot * norm.cdf(d1) - strike * exp(-r * maturity) * norm.cdf(d2)
    return price


# 使用numpy的向量函数重写Black - Scholes公式
def call_option_pricer_nunmpy(spot, strike, maturity, r, Volatility):
    d1 = (np.log(spot / strike) + (r + 0.5 * Volatility * Volatility) * maturity) / Volatility / np.sqrt(maturity)
    d2 = d1 - Volatility * np.sqrt(maturity)

    price = spot * norm.cdf(d1) - strike * np.exp(-r * maturity) * norm.cdf(d2)
    return price


# 计算隐含波动率
# 目标函数，目标价格由target确定
class cost_function:
    def __init__(self, target):
        self.targetValue = target

    def __call__(self, x):
        return call_option_pricer(spot, strike, maturity, r, x) - self.targetValue


if __name__ == '__main__':
    spot = 2.45
    strike = 2.50
    maturity = 0.25
    r = 0.05
    vol = 0.25
    # 假设我们使用vol初值作为目标
    print(u'期权价格 : %.4f' % call_option_pricer(spot, strike, maturity, r, vol))
    target = call_option_pricer(spot, strike, maturity, r, vol)

    cost_sampel = cost_function(target)
    print (u'期权价格： %.2f' % target)
    # 使用sci.Brent算法求解
    impliedVol = brentq(cost_sampel, 0.01, 0.65)
    print(u'期权价格 : %.4f' % call_option_pricer(spot, strike, maturity, r, vol))
    print (u'真实波动率： %.2f' % (vol * 100,) + '%')
    print (u'隐含波动率： %.2f' % (impliedVol * 100,) + '%')
