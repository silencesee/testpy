# encoding:gbk
from __future__ import print_function
import os
import os.path
import sys

reload(sys)
sys.setdefaultencoding('gbk')  # ���ñ������Դ洢����
rootdir = "Z:\\����\Python\\testpy"  # ָ�����������ļ���

for parent, dirnames, filenames in os.walk(rootdir):  # �����������ֱ𷵻�1.��Ŀ¼ 2.�����ļ������֣�����·���� 3.�����ļ�����
    for dirname in dirnames:  # ����ļ�����Ϣ
        print("parent is:" + parent.decode('gbk').encode('utf-8'))
        print("dirname is" + dirname.decode('gbk').encode('utf-8'))

    for filename in filenames:  # ����ļ���Ϣ
        print("parent is" + parent.decode('gbk').encode('utf-8'))
        print("filename is:" + filename.decode('gbk').encode('utf-8'))
        print("the full name of the file is:" + os.path.join(parent.decode('gbk').encode('utf-8'), filename.decode('gbk').encode('utf-8')))  # ����ļ�·����Ϣ
