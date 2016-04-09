#!/usr/bin/python
# -*- coding: utf-8 -*-
__Author__ = 'moxiaoxi'
__Filename__ = 'Subcontracting.py'
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