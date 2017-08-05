# encoding: UTF-8

from data import *
import time
from strategyTog import StrategyTog


if __name__ == '__main__':
    global g_dt_index
    start = time.clock()
    # instruments = ['m', 'rb', 'cu', 'ag', 'bu', 'a', 'c', 'CF', 'i', 'j', 'jm', 'l', 'MA', 'ni', 'p', 'pp', 'RM',
    #                'ru', 'SR', 'TA', 'y', 'zn', 'jd', 'al', 'cs', 'au', 'sn', 'hc', 'ZC', 'OI', 'v', 'pb', 'FG',
    #                'TF']



    product_data= load_data()  # 载入数据
    align_data(product_data)  # 数据对齐

    make_martrix(product_data)  # 数据矩阵化

    strategy_1 = StrategyTog('min15')#策略实例化
    #
    # times = list(g_dt_index['min15'])
    # times.sort()
    #
    # strategy_1.init(instruments, times)
    # strategy_1.process()
    # # cProfile.run('strategy_1.process()', 'myfunction_prof')#性能分析
    #
    # #
    # # strategy_1.statistics()
    # strategy_1.seq_statistics()
    #
    # sharp = strategy_1.calc_sharp()
    # print 'sharp: %f' % sharp
    #
    # end = time.clock()
    # print "use %f s" % (end - start)
    # strategy_1.plot_capital()

    # p = pstats.Stats('myfunction_prof')
    # p.sort_stats('cumtime').print_stats(10)
    # print 'hello'
