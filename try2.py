# encoding: UTF-8
import urllib2
import urllib
from bs4 import BeautifulSoup
import os
import time
j = 1
while True:
    url = 'http://jandan.net/ooxx/page-' + str(j) + '#comments'
    j += 1
    time.sleep(20)
    res = urllib2.urlopen(url)
    html = res.read()
    soup = BeautifulSoup(html, 'html.parser')  # 格式化处理html代码

    result = soup.find_all('img')
    links = []

    for content in result:

        links.append('http:' + content.get('src'))
        imgurl = content.get('src')
        jpgname = imgurl.split('/')[-1]
        if not os.path.exists('photo'):
            os.makedirs('photo')
        i = 0
        for link in links:
            i += 1

            filename = 'photo\\' + jpgname

            with open(filename, 'w') as file:
                urllib.urlretrieve(link, filename)
