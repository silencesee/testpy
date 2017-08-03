# encoding: UTF-8
from __future__ import unicode_literals
import os,sys,pickle,requests
from getsoup import getsoup
from Done.check import checkrep
import time
reload(sys)
sys.setdefaultencoding("utf-8")


j = 1
# 初始化已下载地址数据库
pkfile = sys.argv[0].split('/')[-1][:-3] + '.pkl'
if os.path.exists(pkfile):  # 载入已有的泡菜
    with open(pkfile, 'rb') as pkl_file:
        onlyset = pickle.load(pkl_file)
else:
    onlyset = set()
while True:
    url = 'http://jandan.net/ooxx/page-' + str(j) + '#comments'
    j += 1
    time.sleep(10)

    soup = getsoup(url)  # 格式化处理html代码
    rootpath = 'E:\\我的坚果云\\jandan\\'
    result = soup.find_all('img')
    links = []

    for content in result:

        # links.append('https:' + content.get('src'))
        imgurl = content.get('src')
        jpgname = imgurl.split('/')[-1]
        if checkrep(imgurl, onlyset, pkfile):  # 检查链接是否已经下载过
            if not os.path.exists(rootpath):
                os.makedirs(rootpath)
            filename = rootpath + jpgname
            res = requests.session()
            content0 = res.get('http:'+ imgurl)
            try:
                with open(filename, 'wb') as file:
                # urllib.urlretrieve(link, filename)
                    file.write(content0.content)
            except:
                print '下载失败'
            time.sleep(1.5)
