# -*- coding=gbk -*-
from __future__ import division
from PIL import Image, ImageSequence
import pandas as pd
import random,shutil
import os
from math import sqrt
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Gi(object):
    def __init__(self, input_path, output_path):
        self.inputPath = input_path  # 绝对路径
        self.outputPath = output_path  # 绝对路径
        self.gifInfo = pd.DataFrame()

    def __str__(self):

        return '目标gif信息，调阅请使用object.gifInfo'

    __repr__ = __str__

    def get_target_gif(self, size_gate):
        file_size = []
        full_fname = []
        width = []
        heigh = []
        file_n = []
        del_rate = []
        resize_rate = []
        for parent, dirnames, filenames in os.walk(self.inputPath):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            for filename in filenames:  # 输出文件信息
                if filename[-3:] == 'gif' and filename[0:7] != 'Reverse':
                    pic_path = parent + '\\' + filename
                    full_fname += [pic_path]
                    try:

                        file_format = os.stat(pic_path)  # 获取文件格式
                    except:
                        print ''
                    file_size += [file_format.st_size / 1024 / 1024]  #
                    file_n += [filename]
                    del_rate += [(file_size[-1] - 1.85) / file_size[-1]]
                    resize_rate += [sqrt(2.8 / file_size[-1])]
                    with Image.open(pic_path) as im:
                        (x, y) = im.size
                        width += [x]
                        heigh += [y]

        full_fname = pd.Series(full_fname)
        file_n = pd.Series(file_n)
        gif_b = pd.Series(file_size)
        width = pd.Series(width)
        heigh = pd.Series(heigh)
        del_rate = pd.Series(del_rate)
        resize_rate = pd.Series(resize_rate)
        self.gifInfo = pd.concat([full_fname, file_n, gif_b, width, heigh, del_rate, resize_rate], axis=1)
        self.gifInfo.columns = ['path', 'filename', 'gsize', 'width', 'heigh', 'delRate', 'resizeRate']
        if size_gate > 0:
            self.gifFit = self.gifInfo[self.gifInfo.gsize < size_gate]
            self.gifInfo = self.gifInfo[self.gifInfo.gsize > size_gate]

        return

    def resize(self, w_gate):
        if w_gate == 0:  # 参数为0时，默认将文件目标文件调整到大约2.8M的大小
            if self.inputPath == self.outputPath:
                [(os.popen('gifsicle.exe  --batch  --scale ' + str(x[1].resizeRate) + ' ' + x[1].path)).read() for x in
                 self.gifInfo.iterrows()]
            else:
                [(os.popen(
                    'gifsicle.exe  --scale ' + str(x[1].resizeRate) + ' ' + x[1].path + ' > ' + self.outputPath + '\\' +
                    x[1].filename)).read() for x in self.gifInfo.iterrows()]
                print ''

                [shutil.copy(x, self.outputPath) for x in self.gifFit.path]
            return
        else:

            if self.inputPath == self.outputPath:
                [(os.popen('gifsicle.exe  --batch  --scale ' + str(w_gate) + ' ' + x)).read() for x in
                 self.gifInfo.path]
            else:
                [(
                     os.popen(
                         'gifsicle.exe  --scale ' + str(w_gate) + ' ' + x[1].path + ' > ' + self.outputPath + '\\' + x[
                             1].filename)).read() for x in self.gifInfo.iterrows()]
                [shutil.copy(x, self.outputPath) for x in self.gifFit.path]
            return

    def random_del(self):
        def del_frame(rd_inputpath, rd_outputpath, filename, del_rate):
            # print filename
            with Image.open(rd_inputpath + '\\' + filename) as im:
                frames = [f.copy() for f in ImageSequence.Iterator(im)]
                # pdframe = pd.Series(frames)
                det_num = int(frames.__len__() * del_rate)  # 计算出要删除的帧数
                # choose = raw_input(filename + ' 总帧数' + str(frames.__len__()) + '预计删除' + str(det_num) + '帧，是否继续 Y/N ：\n')
                if det_num / frames.__len__() > 0.4:  #删帧率超过20%则跳过删帧处理，等进一步调整大小
                    return
                del_i_d = [random.randrange(0, frames.__len__()) for i in range(det_num)]  # 计算出保留的对应帧id
                del_i_d = set(del_i_d)
                del_i_d = list(del_i_d)

                del_i_d.sort()

                del_id_str = (map(lambda x1: '#' + str(x1), del_i_d))
                del_id_str = reduce(lambda x2, y2: x2 + ' ' + y2, del_id_str)

                # newFrames = list(pdframe[del_i_d].values)
                # newFrames[0].save(outputpath + '\\' + filename, save_all=True, append_images=newFrames[1:])
                if rd_inputpath == rd_outputpath:
                    cmd = 'gifsicle.exe  --batch' + ' ' + rd_inputpath + '\\' + filename + ' --delete ' + del_id_str
                else:
                    cmd = 'gifsicle.exe ' + rd_inputpath + '\\' + filename + ' --delete ' + del_id_str + ' > ' + rd_outputpath + '\\' + filename
                (os.popen(cmd)).read()
            return

        [del_frame(self.inputPath, self.outputPath, x, y) for x, y in zip(self.gifInfo.filename, self.gifInfo.delRate)]
        return

    def reverse(self):

        [(os.popen('gifsicle.exe ' + x[1].path + ' #-1-0 > ' + self.outputPath + '\\Reverse_' + x[1].filename)).read()
         for x in self.gifInfo.iterrows()]


def resize(re_outputpath):
    resize_gif = Gi(re_outputpath, re_outputpath)
    resize_gif.get_target_gif(2)  # 找出文件大小超过2M的gif
    resize_gif.resize(0)
    if resize_gif.gifInfo.gsize.any():
        check_del(re_outputpath)  # 再递归检查是否符合要求
    return


def check_del(del_outputpath):  #检查目标文件是否符合要求，若不符合则先进行删帧再调整大小
    del_gif = Gi(del_outputpath, del_outputpath)
    del_gif.get_target_gif(2)  # 找出文件大小超过2M的gif
    if del_gif.gifInfo.gsize.any():
        del_gif.random_del()
    if del_gif.gifInfo.gsize.any():
        resize(del_outputpath)
    return


def reverse(re_outputpath):  # 生成倒序播放的图片
    reverse_gif = Gi(re_outputpath, re_outputpath)
    reverse_gif.get_target_gif(0)
    reverse_gif.reverse()
    return


if __name__ == '__main__':
    inputpath = 'E:\\我的坚果云\\初选'
    outputpath = 'E:\\我的坚果云\\已调整'

    sourceGif = Gi(inputpath, outputpath)
    sourceGif.get_target_gif(2)  # 找出文件大小超过2M的gif
    sourceGif.resize(0.8)  # 缩小为原先的0.
    check_del(outputpath)  #检查是否还有超限图片，并递归处理
    reverse(outputpath)
