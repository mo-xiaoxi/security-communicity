#!/usr/bin/python
# -*- coding: utf-8 -*-
__Author__ = 'moxiaoxi'
__Filename__ = 'time.py'
'''
这里定义一个计时相关的函数，用来模拟秒表，衡量性能
使用相关请查看main函数，我给了三个示例
'''

import timeit 

class Timer:
    def __init__(self,func=timeit.default_timer):
        self.elapsed = 0.0
        self._func = func
        self._start = None

    def start(self):
        if self._start is not None:
            raise RuntimeError('Already started')
        self._start = self._func()

    def stop(self):
        if self._start is None:
            raise RuntimeError('Not started')
        end = self._func()
        self.elapsed += end - self._start
        self._start = None

    def reset(self):
        self.elapsed = 0.0 
    @property
    def running(self):
        return self._start is not None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self,*args):
        self.stop()
        return 'stop'



if __name__ =='__main__':
    def countdown(n):
        while n > 0 :
            n -= 1

    #例子  使用start／stop计时
    t = Timer()
    t.start()
    countdown(1000000)
    t.stop()
    print(t.elapsed)

    #例子 使用修饰器进行计时
    with t :
        countdown(1000000)
    print(t.elapsed)

    #例子 引用类
    with Timer() as t2:
        countdown(1000000)
    print(t2.elapsed)