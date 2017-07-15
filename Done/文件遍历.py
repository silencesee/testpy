# encoding:gbk
from __future__ import print_function
import os
import os.path
import sys

reload(sys)
sys.setdefaultencoding('gbk')  # 设置变量可以存储中文
rootdir = "Z:\\开发\Python\\testpy"  # 指明被遍历的文件夹

for parent, dirnames, filenames in os.walk(rootdir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for dirname in dirnames:  # 输出文件夹信息
        print("parent is:" + parent.decode('gbk').encode('utf-8'))
        print("dirname is" + dirname.decode('gbk').encode('utf-8'))

    for filename in filenames:  # 输出文件信息
        print("parent is" + parent.decode('gbk').encode('utf-8'))
        print("filename is:" + filename.decode('gbk').encode('utf-8'))
        print("the full name of the file is:" + os.path.join(parent.decode('gbk').encode('utf-8'), filename.decode('gbk').encode('utf-8')))  # 输出文件路径信息
