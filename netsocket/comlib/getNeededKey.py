#!/usr/bin/python
# -*- coding: utf-8 -*-
__Author__ = 'moxiaoxi'
__Filename__ = 'getNeededKey.py'

'''
当i＝0时，取key前三分之一
当i＝1时，取key中间三分之一
当i＝2时，取key后三分之一
当i不为上述情况或者i和key类型不符合时，raise 输入参数错误
from cryption import getNeededKey
key = '123456789qwertyuio'
for i in range(3):
    an = getNeededKey.getNeededkey1(key,i)
    print an
#123456
#789qwe
#rtyuio
'''
def getKey(key,i):
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
            raise ValueError('2the  argument not allowed')
    else:
        raise ValueError('1the  argument not allowed')

if __name__ == '__main__':
    key = '123456789qwertyuio'
    for i in range(3):
        print getKey(key,i)

