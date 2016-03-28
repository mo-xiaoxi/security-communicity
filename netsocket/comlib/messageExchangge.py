#!/usr/bin/python
# -*- coding: utf-8 -*-
#__Author__ = lixu
#__filename__ = MessageExchangge.py
'''
每次传入一个message
此message必须为偶数，否则爆出异常
当为偶数时候将message一分为二前后交换顺序

#test  messageExchangge
print messageExchangge.m_exchange("abcdefsdfswerd")

>>> 
dfswerdabcdefs
'''

from itertools import cycle, izip

def m_exchange(message):
    _len=len(message)
    if (_len % 2) == 0:
        n=_len/2
        sStr1 = message [n:_len]+message [0:n]
        return sStr1
    else:
        raise "Message Not Even Number Error"
    


if __name__ == '__main__':
    print m_exchange("abcdefsdfswerd")
