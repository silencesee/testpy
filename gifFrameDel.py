# -*- coding=gbk -*-
from __future__ import division
from PIL import Image, ImageSequence
import pandas as pd
import random
import os
import sys

class gi(object):
    def __init__(self,):

def randomDel(parent,filename):
    gifpath = parent + '\\' + filename;
    with Image.open(gifpath) as im:
        frames = [f.copy() for f in ImageSequence.Iterator(im)]
        pdframe = pd.Series(frames)
        detNum = int(frames.__len__() * delRate / 100)  # �����Ҫɾ����֡��
        releastID = [random.randrange(0, frames.__len__()) for i in range(frames.__len__() - detNum)]  # ����������Ķ�Ӧ֡id
        releastID.sort()
        newFrames = list(pdframe[releastID].values)

        newFrames[0].save('out.gif', save_all=True, append_images=newFrames[1:])

        (os.popen('gifsicle.exe  --batch  --scale 0.5  temp.gif ')).read()

        # [f.copy() for f in frames[lastID]]
        # frames.reverse()  # �����б��򷽷�
        # frames[0].save('out1.gif', save_all=True, append_images=frames[1:],quality=100)
        # print( im.format, "%dx%d" % im.size, im.mode)



path = os.path.abspath(os.path.dirname(sys.argv[0]))

delRate = 5
gif_source = '\\gifsource'
gif_output = '\\gifopt'
for parent, dirnames, filenames in os.walk(path+gif_source):  # �����������ֱ𷵻�1.��Ŀ¼ 2.�����ļ������֣�����·���� 3.�����ļ�����
    # for dirname in dirnames:  # ����ļ�����Ϣ
    #     print("��Ŀ¼: ".decode('gbk').encode('utf-8') + parent.decode('gbk').encode('utf-8'))
    #     print("��Ŀ¼ ".decode('gbk').encode('utf-8') + dirname.decode('gbk').encode('utf-8'))

    for filename in filenames:  # ����ļ���Ϣ

        if filename[-3:]=='gif':

            fileFormat = os.stat(parent + '\\' + filename)
            fileSize = fileFormat.st_size / 1024 / 1024
            if fileSize>2:
                randomDel(parent,filename)

