#!/usr/bin/python
# -*- coding: utf-8 -*-
__Author__ = 'moxiaoxi'
__Filename__ = 'AES.py'
def xor(text):
    x = 0x5a
    return ''.join(chr(x^ ord(y)) for y in text)

print xor('we12')
print xor('111')