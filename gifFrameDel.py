# -*- coding=gbk -*-
from __future__ import division
from PIL import Image, ImageSequence
import pandas as pd
import random
import os
import sys


class gi(object):
    def __init__(self, inputPath, outputPath):
        self.inputPath = inputPath
        self.outputPath = outputPath

    def getBigGIF(self):
        abspath = os.path.abspath(os.path.dirname(sys.argv[0]))
        fileSize = []
        fullFname = []
        for parent, dirnames, filenames in os.walk(abspath + self.inputPath):  # �����������ֱ𷵻�1.��Ŀ¼ 2.�����ļ������֣�����·���� 3.�����ļ�����

            for filename in filenames:  # ����ļ���Ϣ

                if filename[-3:] == 'gif':
                    picPath = parent + '\\' + filename
                    fullFname += [picPath]
                    fileFormat = os.stat(picPath)  # ��ȡ�ļ���ʽ
                    fileSize += fileSize + [fileFormat.st_size / 1024 / 1024]  #
                    with Image.open(picPath) as im:
                        (x,y) = im.size
            fullFname=pd.Series(fullFname)
            fileSize = pd.Series(fileSize)
            self.gifInfo = pd.concat([fullFname,fileSize],axis=1)

def randomDel(parent, filename):
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




