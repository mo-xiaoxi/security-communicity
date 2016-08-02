#!/usr/bin/python
# -*- coding: utf-8 -*-
__Author__ = 'moxiaoxi'
__Filename__ = 'Common.py'
"""
在这定义一个迭代类，用于序列号处理
序号范围为0～2^k-1  这里k为8
"""
class Seq(object):   
    def __init__(self, base,number): 
        self.end=2**8-1
        if(base >= self.end):
            raise ValueError("Seq init error ! start {}  end  {}".format(start, end))  
        self.base = base
        self.number = number  
  
    def __iter__(self):   
        return self   
  
    def next(self):  
        r = self.n
        if self.n < self.end:   
            self.n = self.n + 1     
        else:
            self.n = self.start    
        return r
q=Seq(2)
print q.end

"""
Subcontracting
用于对需要传输的信息按bufsiz进行切分

"""
import math

def Subcontracting(msg,bufsize):
    if isinstance(msg,str) and isinstance(bufsize,int):
        datas=[]
        l=int(math.ceil(float(len(msg))/float(bufsize)))
        for i in range(l):
            datas.append(msg[i*bufsize:(i+1)*bufsize])
        datas.append('end')
        return datas
    else:
        print  'the type of argument is error !'
        return 'error'




if __name__ == '__main__':
    print Subcontracting('1234567890',2)
    print Subcontracting('1234567da890',5)