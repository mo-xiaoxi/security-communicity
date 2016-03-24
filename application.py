#!/usr/bin/env python
from itertools import cycle, izip
m1='123'
m1='asdas'
def xor_string(message, key):
    cyphered = ''.join(chr(ord(c)^ord(k)) for c,k in izip(message, cycle(key)))
    # print('%s ^ %s = %s' % (message, key, cyphered))
    return cyphered

if __name__ == '__main__':
    enc = xor_string(m1, m1)
    dec = xor_string(enc, m1)
    print(enc)
    print(dec)