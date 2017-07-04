import hashlib

class Passw(object):

    def __init__(self,source,mode = 'md5',*salt):
        self.source = source
        self.mode = mode
        self.salt = salt
        # self.result = self.cal()

    def __str__(self):
        return 'md5 object : %s' %self.source

    def cal(self):#调用计算函数
        if self.mode == '1':
            str = hashlib.md5()
        elif self.mode == '2':
            str = hashlib.sha1()



            # print(ss)
        str.update(self.source.encode('utf-8'))
            # print(str.hexdigest())
        return str.hexdigest()

    __repr__ = __str__

if __name__=='__main__':
    str = input('请输入密码')
    choose = input('请选择加密模式 1.MD5 2.SHA1')
    s=Passw(str,choose)
    md5str1 = s.cal()
    print('加密结果是：'+md5str1)
    exit()
