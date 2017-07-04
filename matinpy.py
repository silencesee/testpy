from array import array
import math
class Vector2d:
    typecode = 'd'#类属性， 在 Vector2d 实例和字节序列之间转换时使用
    def __init__(self, x, y):#把 x 和 y 转换成浮点数， 尽早捕获错误， 以防调用 Vector2d 函数时传入不当参数。
        self.x = float(x)
        self.y = float(y)
    def __iter__(self):#把 Vector2d 实例变成可迭代的对象， 这样才能拆包（例如， x, y = my_vector）
        return (i for i in (self.x, self.y))
    def __repr__(self):#使用 {!r} 获取各个分量的表示形式， 然后插值， 构成一个字符串； 因为 Vector2d 实例是可迭代的对象， 所以 *self 会把x 和 y 分量提供给 format 函数
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name, *self)
    def __str__(self):
        return str(tuple(self))
    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +
            bytes(array(self.typecode, self)))
    def __eq__(self, other):
        return tuple(self) == tuple(other)
    def __abs__(self):
        return math.hypot(self.x, self.y)
    def __bool__(self):#使用 abs(self) 计算模， 然后把结果转换成布尔值，因此， 0.0 是 False， 非零值是 True
        return bool(abs(self))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])

        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)