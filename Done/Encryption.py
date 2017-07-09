# encoding: UTF-8


import sys
import hashlib


class Encryption(object):
    def __init__(self, source, mode='md5', *salt):
        self.source = source
        self.mode = mode
        self.salt = salt
        # self.result = self.cal()

    def __str__(self):
        return 'md5 object : %s' % self.source

    def cal(self):  # 调用计算函数
        temper=''
        if self.mode == '1':
            temper = hashlib.md5()
        elif self.mode == '2':
            temper = hashlib.sha1()
        temper.update(self.source.encode('utf-8'))
        return temper.hexdigest()

    __repr__ = __str__


if __name__ == '__main__':
    if '2.7' in sys.version:
        password_str = raw_input('请输入密码: ')
        choose = raw_input('请选择加密模式 1.MD5 2.SHA1 :')
    else:
        password_str = input('请输入密码: ')
        choose = input('请选择加密模式 1.MD5 2.SHA1 :')

    s = Encryption(password_str, choose)
    md5str1 = s.cal()
    print('加密结果是：' + md5str1)
    exit()
