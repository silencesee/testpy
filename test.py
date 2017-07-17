# encoding: UTF-8
# 构建装饰器

import functools


def params_chack(*types, **kwtypes):
    def _outer(func):
        @functools.wraps(func)
        def _inner(*args, **kwargs):
            result = [isinstance(_param, _type) for _param, _type in zip(args, types)]
            assert all(result), "参数类型申明错误"
            result = [isinstance(kwargs[_param], kwtypes[_param]) for _param in kwargs if _param in kwtypes]
            assert all(result), "参数类型申明错误"
            return func(*args, **kwargs)

        return _inner

    return _outer


# 使用装饰器
@params_chack(int, str, c=(int, str))
def test04(a, b, c):
    print("in function test04, a=%s, b=%s, c=%s" % (a, b, c))
    return 1


# 测试用例
print(test04(1, "str", 1))  # 参数正确
print(test04(1, "str", "abc"))  # 参数正确
print(test04("str", 1, "abc"))  # 参数错误
