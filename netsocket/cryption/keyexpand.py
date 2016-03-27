#!/usr/bin/python
# -*- coding: utf-8 -*-
#__Author__ = lixu
#__filename__ = keyExchangge.py
'''
每次传入message信息与key异或处理生成新的密钥_key。
然后返回_key

#test  keyExpand
k="1231231231231231"
m="m1"

>>> 
_KPTR   ZGRU\

'''


from itertools import cycle, izip

def xor_string(message, key):
    
    #message=message[0:48]
    _key = ''.join(chr((ord(c)^ord(k))) for c,k in izip(message, cycle(key)))
    # print('%s ^ %s = %s' % (message, key, cyphered))
    
    return _key

if __name__ == '__main__':
    k="123456789123456712345678912345671234567891234567"
    m="m114333333333333333333333333333333333333333333"
    enc = xor_string(m, k)
    dec = xor_string(enc, m)
    print len(k)
    print len(enc)
    print(enc)
    print(dec)
