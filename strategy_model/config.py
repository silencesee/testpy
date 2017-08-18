# encoding: UTF-8
# 需要读取的品种
# instruments = ['m', 'rb', 'cu', 'ag', 'bu', 'a', 'c', 'CF', 'i', 'j', 'jm', 'l', 'MA', 'ni', 'p', 'pp', 'RM',
#                'ru', 'SR', 'TA', 'y', 'zn', 'jd', 'al', 'cs', 'au', 'sn', 'hc', 'ZC', 'OI', 'v', 'pb', 'FG',
#                'TF']
# instruments = ['rb', 'cu', 'ag', 'bu', 'a', 'c', 'CF', 'i', 'j', 'jm', 'l', 'MA', 'ni', 'p', 'pp', 'RM', 'ru', 'SR', 'TA', 'y', 'zn']
instruments = ['m', 'rb', 'cu']
# 需要读取的周期,是一个列表，框架支持载入多个周期数据,格式tick,min1,mi5,min15,min30,min60,day,week
periods = ['min30']
# 指定策略运行的基础周期，字符串，唯一值
basic_period = periods[0]
# 每个品种分配的资金
money = 100000
# 滑点
slip = 2
# 冲击成本
costRate = 2 / 10000
# 配置策略中需要的因子
factor = ['close']
