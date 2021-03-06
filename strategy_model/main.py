# encoding: UTF-8

from data import *
from strategy import Strategy_Inst
from analysis import *

if __name__ == '__main__':
    start = time.time()
    #  数据初始化
    product_data = load_data()  # 载入数据
    timelist, dataKeys = align_data(product_data)  # 数据对齐，并且输出配置数据里面指定的基频时间轴
    matrix = make_matrix(product_data)  # 数据矩阵化
    print ('载入%s数据耗时 [%0.8fs]' %(instruments,time.time()-start))
    #  策略初始化
    strategy_1 = Strategy_Inst(timelist, dataKeys)  # 策略实例化

    strategy_1._run()
    # # cProfile.run('strategy_1.process()', 'myfunction_prof')#性能分析
    #
    # #
    # # strategy_1.statistics()

    result = Statistics(strategy_1.recorder)
    # result.netprofit()
    # result.netprofit_single('rb')
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
