# encoding: UTF-8
# 这个图集比较邪恶
from __future__ import unicode_literals

import os
import pickle
import re
import sys
import urllib,time,random

from Done.check import checkrep
from getsoup import getsoup

reload(sys)
sys.setdefaultencoding("utf-8")


#初始化已下载地址数据库
pkfile = sys.argv[0].split('/')[-1][:-3]+'pkl'
if os.path.exists(pkfile):  # 载入已有的泡菜
    with open(pkfile, 'rb') as pkl_file:

        onlyset = pickle.load(pkl_file)
else:
    onlyset = set()
# 初始化下载目录
rootpath = 'E:\\我的坚果云\\7kk'
j = 0
urlbegin = 'http://www.7kk.com/album/photos/70022.html'
if not os.path.exists(rootpath):
    os.makedirs(rootpath)
while True:


    soup = getsoup(urlbegin)
    if checkrep(urlbegin, onlyset, pkfile):# 检查图片链接是否已经下载过
        result = soup.find_all('div', attrs={'class': 'imgholder'})
        for contens in result:  # 轮询主题地址
            if 'picture' in contens.find('a').get('href'):

                soup0 = getsoup('http://www.7kk.com' + contens.find('a').get('href'))
                result0 = soup0.find('a', attrs={'class': 'bizhi-img'})
                source = result0.find('img').get('src')
                filename = source.split('/')[-1]
                filename = re.sub(r'[\\\\/\:\*\?\"\<\>\|\,]+(\,[^\\\\/\:\*\?\"\<\>\|\,]+)*', '', filename)  # 处理不合规的文件名称
                if not os.path.exists(rootpath+'\\'+filename):
                    time.sleep(random.choice(range(5)))
                    urllib.urlretrieve(source.encode('ascii'), rootpath+'\\'+filename)


    nextpage = soup.find('a', attrs={'class': 'nextBtn'})

    urlbegin = 'http://www.7kk.com' + nextpage.get('href')  # 下一个图集



    # for index in source[u'picInfo']:
