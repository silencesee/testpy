# encoding: UTF-8
# 网站=gifjia，gif更新很慢，偶尔抓取就好
from __future__ import unicode_literals

import os
import pickle
import sys

import requests

from Done.check import *
from getsoup import getsoup

reload(sys)
sys.setdefaultencoding("utf-8")
import time

def downpic(url, path):
    try:
        soup = getsoup(url)
    except:
        pass
    source = soup.find_all('img',attrs={'class':"aligncenter",'src':re.compile(r'.*\.gif')})
    if isempty(source):
        source = soup.find('article').find_all('img', attrs={'src': re.compile(r'.*\.gif')})

    for pic in source:


        link = pic.get('src')
        filename = pic.get('alt')+link.split('/')[-1]

        filename=namefix(filename)
        path0=path+filename
        if not os.path.exists(path0):
            print filename
            time.sleep(2)
            resq = requests.session()
            web = resq.get(link)
            with open(path0, 'wb') as f:

                f.write(web.content)
                # print '下载 ：' + tempname + '.gif'



j = 1
# 初始化已下载地址数据库
pkfile = sys.argv[0].split('/')[-1][:-3] + 'pkl'
if os.path.exists(pkfile):  # 载入已有的泡菜
    with open(pkfile, 'rb') as pkl_file:
        onlyset = pickle.load(pkl_file)
else:
    onlyset = set()
# 初始化下载目录
rootpath = 'E:\\我的坚果云\\gifjia'
if not os.path.exists(rootpath):
    os.makedirs(rootpath)
while True:
    # time.sleep(20)
    url = 'http://www.gifjia.com/baoxiaogif/page/' + str(j) + '/'
    j += 1  #
    time.sleep(2)
    try:

        soup = getsoup(url)  # 格式化处理html代码
    except:
        pass
    result = soup.find_all('article')

    for contens in result:  # 轮询图集地址
        title = contens.find('h2').find('a').get('title')
        href = contens.find('h2').find('a').get('href')
        print title
        if checkrep(href, onlyset, pkfile):  # 检查链接是否已经下载过 checkrep(href, onlyset, pkfile)
            if not os.path.exists(rootpath + '\\' + title.decode('utf-8')):  # 创建图集主题文件夹
                os.makedirs(rootpath + '\\' + title.decode('utf-8'))
            time.sleep(2)
            soup0 = getsoup(href)  # 格式化处理html代码
            contens0 = soup0.find_all('div', attrs={'article-paging'})[0]
            source_link=(map(lambda x:x.get('href'),contens0.find_all('a')))
            source_link.append(href)
            path = rootpath + '\\' + title + '\\'
            [downpic(url, path) for url in source_link]
