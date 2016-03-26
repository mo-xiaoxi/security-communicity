#!/usr/bin/python
# -*- coding: utf-8 -*-
#__Author__ = lixu
#__filename__ = packetfill.py
'''
packetFill
传入一个message
随即填充长度为0-0xff的字符串
返回新的字符串和原字符串长度

re_packetFill
传入一个字符串，和对应message的长度
返回原massage的内容

#test  packetFill
message='1231'
x=987987
m,y=packetFill.packetFill(message,x)
print m,y
print packetFill.re_packetFill(m,y)

>>>

00987987000000041231(这里的随机填充)  4
('1231', 987987)


'''

from itertools import cycle, izip
import random

def packetFill(message,seq):
    m_length=len(message)
    length_=random.randint(0,0xFF)
    message=message+''.join(chr(random.randint(0, 0xFF)) for i in range(length_))
    _length=len(message)
    if (_length % 2) != 0:
        message=message+chr(random.randint(0, 0xFF))
    seq=str(seq)
    seq=seq.zfill(8)
    bm_length=str(m_length)
    bm_length=bm_length.zfill(8)
    message=seq+bm_length+message
    return message,m_length
    
def re_packetFill(message,m_length):
    m_len=int(message[0:8])
    message=message[16:16+m_length]
    return message,m_len
    

if __name__ == '__main__':
    message='1231'
    x=987987
    m,y=packetFill(message,x)
    print m,y
    print re_packetFill(m,y)
