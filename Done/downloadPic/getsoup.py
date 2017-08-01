# encoding: UTF-8
from __future__ import unicode_literals
import urllib2
from bs4 import BeautifulSoup
def getsoup(url):
    res = urllib2.urlopen(url)
    html = res.read()
    soup = BeautifulSoup(html, 'html.parser')  # 格式化处理html代码
    return soup