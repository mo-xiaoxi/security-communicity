#!/usr/bin/python
# -*- coding: utf-8 -*-
__Author__ = 'moxiaoxi'
__Filename__ = 'getNeededKey.py'
def getNeededkey1(key,i):
    l=len(key)
    if  isinstance(key,str) and isinstance(i,int) and l%3 == 0 :
        l/=3
        if(i==0):
            return key[0:l]
        elif(i==1):
            return key[l:2*l]
        elif(i==2):
            return key[2*l:3*l]
        else:
            raise ValueError('the  argument not allowed')
    else:
        raise ValueError('the  argument not allowed')

if __name__ == '__main__':
    key = '123456789qwertyuio'
    for i in range(3):
        print getNeededkey1(key,i)

