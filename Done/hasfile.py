# encoding: UTF-8
import hashlib
import os, sys


def CalcSha1(filepath):
    with open(filepath, 'rb') as f:
        sha1obj = hashlib.sha1()
        sha1obj.update(f.read())
        hash = sha1obj.hexdigest()
        print(hash)
        return hash


def CalcMD5(filepath):
    with open(filepath, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash = md5obj.hexdigest()
        print(hash)
        return hash


if __name__ == "__main__":


    CalcMD5('Z:\\develop\\python\\testpy\\Done\\24f3432b2d2626568658fbbad8ae6.gif')
