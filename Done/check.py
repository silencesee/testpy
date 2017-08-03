# encoding: UTF-8
import pickle, re, json,time,random
from Done.Encryption import Encryption


def checkrep(uri, onlyset, pkfile):  # 通过pickle文件检查历史重复记录
    hasvalue = Encryption(uri, '1').cal()
    if not hasvalue in onlyset:
        onlyset.add(hasvalue)
        with open(pkfile, 'wb') as output:
            pickle.dump(onlyset, output)
            print '访问 '+uri
            time.sleep(random.choice(range(5)))
        return True
    else:
        print '已访问 ' + uri
        time.sleep(random.choice(range(10)))
        return False


def namefix(oldname):  # 检查并修复文件名称中不合法的字符串
    newname = re.sub(r'[\\\\/\:\*\?\"\<\>\|\,]+(\,[^\\\\/\:\*\?\"\<\>\|\,]+)*', '', oldname)  # 处理不合规的文件名称
    return newname


def jsonfix(oldjson):  # 检查并修复json文件里面不合法的字符如\n\r
    html1 = re.sub(r'\s', '', oldjson)
    newjson = json.loads(html1)
    return newjson


def isempty(object):  # 检查变量是否为空值
    if len(object) == 0:
        return True
    else:
        return False
