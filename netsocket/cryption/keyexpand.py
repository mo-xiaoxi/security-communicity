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
    _key = ''.join(chr(ord(c)^ord(k)) for c,k in izip(message, cycle(key)))
    # print('%s ^ %s = %s' % (message, key, cyphered))
    return _key

if __name__ == '__main__':
    k="1231231231231231"
    m="m1"
    enc = xor_string(k, m)
    dec = xor_string(enc, m)
    print(enc)
    print(dec)
