# encoding: UTF-8
# instruments = ['m', 'rb', 'cu', 'ag', 'bu', 'a', 'c', 'CF', 'i', 'j', 'jm', 'l', 'MA', 'ni', 'p', 'pp', 'RM',
#                'ru', 'SR', 'TA', 'y', 'zn', 'jd', 'al', 'cs', 'au', 'sn', 'hc', 'ZC', 'OI', 'v', 'pb', 'FG',
#                'TF']
instruments = ['m', 'rb', 'cu']  # 需要读取的品种
periods = ['min15']  # 需要读取的周期,是一个列表，框架支持载入多个周期数据,格式tick,min1,mi5,min15,min30,min60,day,week
basic_period = periods[0]  #  指定策略运行的基础周期，字符串，唯一值
