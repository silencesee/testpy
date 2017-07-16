# -*- coding=utf-8 -*-
from __future__ import division
from PIL import Image, ImageSequence
import pandas as pd
import random
import os
import sys
from math import sqrt
import numpy as np


class gi(object):
    def __init__(self, inputPath, outputPath):
        self.inputPath = inputPath  # 绝对路径
        self.outputPath = outputPath  # 绝对路径

    def __str__(self):

        return '目标gif信息，调阅请使用object.gifInfo'

    __repr__ = __str__

    def GetBigGIF(self, sizeGate):
        abspath = os.path.abspath(os.path.dirname(sys.argv[0]))
        fileSize = []
        fullFname = []
        width = []
        heigh = []
        fileN = []
        delRate = []
        resizeRate=[]
        for parent, dirnames, filenames in os.walk(self.inputPath):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            for filename in filenames:  # 输出文件信息
                if filename[-3:] == 'gif':
                    picPath = parent + '\\' + filename
                    fullFname += [picPath]
                    fileFormat = os.stat(picPath)  # 获取文件格式
                    fileSize += [fileFormat.st_size / 1024 / 1024]  #
                    fileN += [filename]
                    delRate += [(fileSize[-1]-1.85) / fileSize[-1]]
                    resizeRate += [sqrt(2.8/fileSize[-1])]
                    with Image.open(picPath) as im:
                        (x, y) = im.size
                        width += [x]
                        heigh += [y]

            fullFname = pd.Series(fullFname)
            fileN = pd.Series(fileN)
            gifB = pd.Series(fileSize)
            width = pd.Series(width)
            heigh = pd.Series(heigh)
            delRate = pd.Series(delRate)
            resizeRate = pd.Series(resizeRate)
            self.gifInfo = pd.concat([fullFname, fileN, gifB, width, heigh,delRate,resizeRate], axis=1)
            self.gifInfo.columns = ['path', 'filename', 'gsize', 'width', 'heigh', 'delRate','resizeRate']
            self.gifInfo = self.gifInfo[self.gifInfo.gsize > 2]
        return

    def resize(self, wGate):
        if wGate==0:
            if self.inputPath == self.outputPath:
                [(os.popen('gifsicle.exe  --batch  --scale ' + str(y) + ' ' + x)).read() for x in self.gifInfo.path  for y in self.gifInfo.resizeRate]
            else:
                [(os.popen('gifsicle.exe  --scale ' + str(y) + ' ' + x[1].path + ' > ' + self.outputPath + '\\' + x[1].filename)).read() for x in self.gifInfo.iterrows() for y in self.gifInfo.resizeRate]
            return
        else:

            if self.inputPath == self.outputPath:
                [(os.popen('gifsicle.exe  --batch  --scale ' + str(wGate) + ' ' + x)).read() for x in self.gifInfo.path]
            else:
                [(os.popen('gifsicle.exe  --scale ' + str(wGate) + ' ' + x[1].path + ' > ' + self.outputPath + '\\' + x[
                    1].filename)).read() for x in self.gifInfo.iterrows()]
            return

    def randomDel(self):
        def delframe(inputpath, outputpath, filename,delRate):
            # print filename
            with Image.open(inputpath + '\\' + filename) as im:
                frames = [f.copy() for f in ImageSequence.Iterator(im)]
                pdframe = pd.Series(frames)
                detNum = int(frames.__len__() * delRate)  # 计算出要删除的帧数
                choose = raw_input(filename +' 总帧数'+str(frames.__len__())+ '预计删除' + str(detNum) + '帧，是否继续 Y/N ：\n')
                if choose.upper() == 'N': return
                delID = [random.randrange(0, frames.__len__()) for i in range(detNum)]  # 计算出保留的对应帧id
                delID = set(delID)
                delID = list(delID)

                delID.sort()

                f = lambda x: '#' + str(x)
                delID_str = (map(f, delID))
                delID_str = reduce(lambda x, y: x + ' ' + y, delID_str)

                # newFrames = list(pdframe[delID].values)
                # newFrames[0].save(outputpath + '\\' + filename, save_all=True, append_images=newFrames[1:])
                if inputpath == outputpath:
                    cmd = 'gifsicle.exe  --batch' + ' ' + inputpath + '\\' + filename + ' --delete ' + delID_str
                else:
                    cmd = 'gifsicle.exe ' + inputpath + '\\' + filename + ' --delete ' + delID_str + ' > ' + outputpath + '\\' + filename
                (os.popen(cmd)).read()
            return

        [delframe(self.inputPath, self.outputPath, x,y) for x in self.gifInfo.filename for y in self.gifInfo.delRate]
        return


def resize(outputpath):
    resizeGIF = gi(outputpath, outputpath)
    resizeGIF.GetBigGIF(2)  # 找出文件大小超过2M的gif
    resizeGIF.resize(0)
    checkDel(outputpath)


def checkDel(outputpath):
    delGIF = gi(outputpath, outputpath)
    delGIF.GetBigGIF(2)  # 找出文件大小超过2M的gif
    delGIF.randomDel()
    resize(outputpath)


if __name__ == '__main__':
    inputpath = 'Z:\\develop\\python\\testpy\\gifsource'
    outputpath = 'Z:\\develop\\python\\testpy\\gitopt'
    sourceGif = gi(inputpath, outputpath)
    sourceGif.GetBigGIF(2)  # 找出文件大小超过2M的gif
    sourceGif.resize(0.8)  # 缩小为原先的0.
    checkDel(outputpath)
