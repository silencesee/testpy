# encoding: UTF-8
# 新浪的数据是直接通过json下载，请求信息在json地址里面
from __future__ import unicode_literals

import json
import os
import pickle
import re
import sys
import urllib
import urllib2

from Done.check import *

reload(sys)
sys.setdefaultencoding("utf-8")

j = 0
repcount = 0
# 初始化已下载地址数据库
pkfile = sys.argv[0].split('/')[-1][:-3] + 'pkl'
if os.path.exists(pkfile):  # 载入已有的泡菜
    with open(pkfile, 'rb') as pkl_file:

        onlyset = pickle.load(pkl_file)
else:
    onlyset = set()
# 初始化下载目录
rootpath = 'E:\\我的坚果云\\sina'
if not os.path.exists(rootpath):
    os.makedirs(rootpath)
while True:
    # time.sleep(20)
    j += 1  # 每页展示30个主题，循环一遍后偏移量+30
    uri = 'http://platform.sina.com.cn/slide/album?app_key=2733610594&format=json&ch_id=77&num=20&page=' + str(
        j) + '&jsoncallback=getDataJson'  # 获取json地址
    # 处理json

    res0 = urllib2.urlopen(uri)
    html0 = res0.read()
    html0 = html0.decode('unicode_escape')
    source = json.loads(html0[12:-1])
    for pic in source[u'data']:  # 批量下载图片并按照标题命名
        filename =pic[u'name'] + '.gif'
        filename =  rootpath+'\\'+ namefix(filename)  # 处理不合规的文件名称
        temp_adress = pic[u'img_url']
        temp_adress = temp_adress.split('/')
        source_adress = 'http://storage.slide.news.sina.com.cn/slidenews/77_ori/' + temp_adress[-2] + '/' + \
                        temp_adress[-1]
        if checkrep(source_adress, onlyset, pkfile):  # 检查链接是否已经下载过
            if not os.path.exists(filename.decode('utf-8')):  # 检查文件是否存在
                urllib.urlretrieve(source_adress.encode('ascii'), filename)
