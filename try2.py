# encoding: UTF-8
class MyClass:
    val1 = 'Value 1'
    def __init__(self):
        self.val2 = 'Value 2'
    @staticmethod
    def cmpp(self):
        print 'ces'
    def diaoyon(self):
        cmpp
    @staticmethod
    def staticmd():
        print '静态方法，无法访问val1和val2'

    @classmethod
    def classmd(cls):
        print '类方法，类：' + str(cls) + '，val1：' + cls.val1
        print '类方法，类：' + str(cls) + '，val1：' + cls.val2
if __name__ == '__main__':
    mc = MyClass()  # 实例化
    mc.staticmd()
    mc.classmd()