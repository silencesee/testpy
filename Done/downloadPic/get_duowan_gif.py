# encoding: UTF-8
# 先通过页面获得图集主题，在主题间循环，并在主题内通过json下载图片
from __future__ import unicode_literals

import json
import os
import pickle
import re
import sys
import time
import urllib
import urllib2

from Done.check import checkrep
from getsoup import getsoup

reload(sys)
sys.setdefaultencoding("utf-8")
j = 0
# 初始化已下载地址数据库
pkfile = sys.argv[0].split('/')[-1][:-3] + 'pkl'
if os.path.exists(pkfile):  # 载入已有的泡菜
    with open(pkfile, 'rb') as pkl_file:
        onlyset = pickle.load(pkl_file)
else:
    onlyset = set()
# 初始化下载目录
rootpath = 'E:\\我的坚果云\\duowan'
if not os.path.exists(rootpath):
    os.makedirs(rootpath)
while True:

    url = 'http://tu.duowan.com/m/bxgif?offset=' + str(j)
    j += 30  # 每页展示30个主题，循环一遍后偏移量+30
    soup = getsoup(url)  # 格式化处理html代码
    result = soup.find_all('em')
    result2 = soup.find_all('span', {'class': 'fr'})

    for contens in zip(result[1:], result2):  # 轮询图集地址
        try:
            title = contens[0].find('a').renderContents()
            href = contens[0].find('a').get("href")
            if checkrep(href, onlyset, pkfile):  # 检查链接是否已经下载过
                if not os.path.exists(rootpath + '\\' + title.decode('utf-8')):  # 创建图集主题文件夹
                    os.makedirs(rootpath + '\\' + title.decode('utf-8'))
                str = href.split('/')[-1]  # 获取主题网页关键ID
                uri = 'http://tu.duowan.com/index.php?r=show/getByGallery/&gid=' + str[:-5]  # 构造json地址
                # 处理json
                res0 = urllib2.urlopen(uri)
                html0 = res0.read()
                html0 = html0.decode('unicode_escape')
                try:
                    source = json.loads(html0)
                except:
                    try:


                        html0 = html0.replace('\r\n', '')
                        debughtm = re.sub(r'\bmp4_url":".*?","sort\b', 'mp4_url":" ","sort',
                                          html0)  # 处理json不兼容的\r\n情况，替换错误部分为空值
                        source = json.loads(debughtm)
                    except:
                        print html0
                        raise '出现错误'
                        time.sleep(20)
                for pic in source[u'picInfo']:  # 批量下载图片并按照标题命名
                    filename = pic[u'add_intro'] + '.gif'
                    filename = re.sub(r'[\\\\/\:\*\?\"\<\>\|\,]+(\,[^\\\\/\:\*\?\"\<\>\|\,]+)*', '',
                                      filename)  # 处理不合规的文件名称
                    source_adress = pic[u'source']
                    path = rootpath + '\\' + title + '\\' + filename
                    if not os.path.exists(path):
                        urllib.urlretrieve(source_adress.encode('ascii'), path)
                time.sleep(10)
        except:
            pass
