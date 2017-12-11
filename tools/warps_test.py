# -*-coding=utf-8 -*-
__author__ = 'piay'
import functools, time
'''
一个函数执行前打印开始执行，执行完后打印执行完成，记录执行时间
'''

def log(text):
    if callable(text):  # 参数如果是函数，说明装饰器不带参传过来,text是一个函数
        @functools.wraps(text)
        def wrapper(*args, **kwargs):
            start = time.clock()
            print '这是不带参数的装饰器,开始执行'
            f = text(*args, **kwargs)  #执行本身的函数 text（）
            end = time.clock()
            print "结束执行:", end - start
            return f  # 返还原函数
        return wrapper

    elif not callable(text):  # text是参数，不是函数
        def decarator(func):
            @functools.wraps(func)
            def warpper(*args, **kwargs):
                start = time.clock()
                print '这是不带参数的装饰器,开始执行,参数为：'+text
                f = func(*args, **kwargs)
                end=time.clock()
                print "结束执行:",end-start
                return f  #返还原函数
            return warpper
        return decarator
    else:
        print '请检查是否正确'


@log
def add1(x,y):
    print x+y

@log('222')
def add2(x,y):
    print  x+y
#
# add1(1,2)
# add2(2,3)



def decorator_whith_params_and_func_args(arg_of_decorator):
    def handle_func(func):
        def handle_args(*args, **kwargs):
            print "begin"
            func(*args, **kwargs)
            print "end"
            print arg_of_decorator, func, args,kwargs
        return handle_args
    return handle_func


@decorator_whith_params_and_func_args("123")
def foo4(a, b=2):
    print "Content"

foo4(1, b=3)