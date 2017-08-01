# encoding: UTF-8
import urllib2
import urllib
from bs4 import BeautifulSoup
import os,sys,pickle
from Done.check import checkrep
import time
j = 1
# 初始化已下载地址数据库
pkfile = sys.argv[0].split('/')[-1][:-3] + 'pkl'
if os.path.exists(pkfile):  # 载入已有的泡菜
    with open(pkfile, 'rb') as pkl_file:
        onlyset = pickle.load(pkl_file)
else:
    onlyset = set()
while True:
    url = 'http://jandan.net/ooxx/page-' + str(j) + '#comments'
    j += 1
    time.sleep(10)
    res = urllib2.urlopen(url)
    html = res.read()
    soup = BeautifulSoup(html, 'html.parser')  # 格式化处理html代码
    rootpath = 'E:\\我的坚果云\\jandan\\'
    result = soup.find_all('img')
    links = []

    for content in result:

        links.append('http:' + content.get('src'))
        imgurl = content.get('src')
        jpgname = imgurl.split('/')[-1]
        if checkrep(imgurl, onlyset, pkfile):  # 检查链接是否已经下载过
            if not os.path.exists(rootpath):
                os.makedirs(rootpath)
            i = 0
            for link in links:
                i += 1

                filename = rootpath + jpgname

                with open(filename, 'w') as file:
                    urllib.urlretrieve(link, filename)
