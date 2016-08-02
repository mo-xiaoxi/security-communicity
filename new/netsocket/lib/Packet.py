#!usr/bin/env python
# -*- coding:utf-8 -*-
__Filename__='Packet.py'



import hmac
import struct 
import random
from itertools import cycle,izip
from Crypto.Cipher import AES
from Crypto import Random
from binascii import b2a_hex,a2b_hex

'''
包封装过程:
key: aeskey(16)|hmackey1(16)|hmackey2(16) 一共48位
------------------------------------------------
data1:  msg (这里保证输入的msg少于996位)
================================================>
data2:  Seq(8)|Len(8)|message|randstring(rand)   
这里需保证data2的位数为偶数，具体需要在rand填充中做处理；此外，填充的时候，还需要考虑填充后的长度不能超过996位
================================================>
data3: padding(AESOUT(data2,aeskey1))|HMAC(data2,hmackey1) 1024位一个包 前面需要填充至996
================================================>
packet: data3
================================================>
local_ack:HMAC(hmackey2,exchange(aesout))
'''
MAX_SEQENCE_NUMBER = 512
PACKET_SIZE = 1024

class Packet(object):
    '打包数据包和解开数据包操作'

    def __init__(self,msg,seq,key):
        '这里需要检查下输入的msg,seq,key是否符合规范，还未实现'
        self.key = key
        self.seq = seq
        self.msg = msg
        self.aeskey = key[0:15]
        self.hmackey1 = key[16:31]
        self.hmackey2 = key[32:47]
        self.data1 = msg
        self.data2 = ''
        self.data3 = ''
        self.local_ack=''
        self.aesout = ''
        self.HMAC1 = ''
        self.HMAC2 = ''#这里想着封装成一个类，方便调试与后期添加功能
  
    def __iter__(self):   
        return self   
        
    def make_pkt(self):
        '打包'
        self.data2 = PacketFill(self.msg,self.seq)
        self.aesout = ''#AES(self.data2,self.aeskey)
        self.HMAC1 = ''#HMAC(self.data2,self.hmackey1)
        self.data3 = self.aesout+self.HMAC1
        self.HMAC2 = ''#HMAC(m_exchange(self.data3),self.hmackey2)
        self.data4 = struct.pack("<1024s32s", self.aesout, self.HMAC2)
        return packet,ack

    def extract_pkt():
        '解包'
        pass


    def PacketFill(message,seq):
        '包随机填充，需保证填充后的位数为偶数，且不超过996位'
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
        return message

    def Re_PacketFill(message):
        m_length=int(message[8:16])
        seq=int(message[0:8])
        message=message[16:16+m_length]
        return message,seq

    def AESEncrypt(self):
        pass

    def AESDecrypt(self):
        pass

    def m_exchange(message):
        '信息前后交换:123456===>456123,message必须为偶数'
        _len=len(message)
        if (_len % 2) == 0:
        n=_len/2
        sStr1 = message [n:_len]+message [0:n]
        return sStr1
    else:
        raise "Message Not Even Number , Error!"

    def hmac_md5():
        pass