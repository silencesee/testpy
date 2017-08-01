# encoding: UTF-8
# 从内涵段子的json下载
from __future__ import unicode_literals

import os
import pickle
import sys
import urllib2

import requests
import time

from Done.check import *

reload(sys)
sys.setdefaultencoding("utf-8")

j = 0
repcount = 0
# 初始化已下载地址数据库
pkfile = sys.argv[0].split('/')[-1][:-3] + '.pkl'
if os.path.exists(pkfile):  # 载入已有的泡菜
    with open(pkfile, 'rb') as pkl_file:
        onlyset = pickle.load(pkl_file)
else:
    onlyset = set()
# 初始化下载目录
rootpath = 'E:\\我的坚果云\\neihanduanzi'
if not os.path.exists(rootpath):
    os.makedirs(rootpath)

numfile = sys.argv[0].split('/')[-1][:-3] + '_num.pkl'
if os.path.exists(numfile):  # 载入已有的泡菜
    with open(numfile, 'rb') as num_file:
        num = pickle.load(num_file)
        print '起始页编号'+str(num)
else:
    num = '1501413454'
while True:
    time.sleep(10)
    j += 1  # 每页展示30个主题，循环一遍后偏移量+30
    uri = 'http://neihanshequ.com/pic/?is_json=1&app_name=neihanshequ_web&max_time='+str(num)
    # 处理json

    res0 = urllib2.urlopen(uri)
    html0 = res0.read()
    html0 = html0.decode('unicode_escape')
    try:
        source = json.loads(html0)
    except:
        try:
            source = jsonfix(html0)
        except Exception,e:
            print e
            continue

    for pic in source['data']['data']:  # 批量下载图片并按照标题命名
        if pic['group']['category_id']==10:
            try:

                temp_adress = pic['group']['large_image']['url_list'][0]['url']
            except:
                try:
                    temp_adress = pic['group']['large_image_list'][1]['url_list'][0]['url']

                except:
                    continue

            if checkrep(temp_adress, onlyset, pkfile):  # 检查链接是否已经下载过
                tempname = pic['group']['content']
                tempname = namefix(tempname)  # 处理不合规的文件名称
                filename =  rootpath+'\\'+temp_adress.split('/')[-1]+ tempname+ '.gif'
                if not os.path.exists(filename.decode('utf-8')):  # 检查文件是否存在
                    resq=requests.session()
                    web=resq.get(temp_adress)
                    with open(filename,'wb') as f:
                        f.write(web.content)
                        print '下载 ：'+tempname+'.gif'
                else:
                    print '文件已存在'+tempname
            else:
                print '链接已下载'+temp_adress
        else:
            print '链接不是gif，跳过下载'
    num = source['data'][u'max_time']
    with open(numfile, 'wb') as num_file:
        pickle.dump(num,num_file)
        print '记录已完成的页面'+str(num)+'\n'

