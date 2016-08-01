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
key: aeskey1(16)|hmackey2(16)|hmackey3(16) 一共48位
------------------------------------------------
data1:  msg (这里保证输入的msg少于996位)
================================================>
data2:  Seq(8)|Len(8)|message|randstring(rand)   
这里需保证data2的位数为偶数，具体需要在rand填充中做处理；此外，填充的时候，还需要考虑填充后的长度不能超过996位
================================================>
data3: AESOUT(data2,aeskey1)|HMAC(data2,hmackey2)
================================================>
data4: padding(data3to996)|HMAC(exchange(data3),hmackey3) 即一共1024位一个包,exchange为将包前后翻转一下
================================================>
packet: data4

'''
MAX_SEQENCE_NUMBER = 512
PACKET_SIZE = 1024

class Packet(object):
    '打包数据包和解开数据包操作'
    def __init__(self,seq,key,msg):
        self.key = key
        self.seq = seq
        self.msg = msg
        self.aeskey = ''
        self.hmackey1 = ''
        self.hmackey2 = ''
        self.data1 = msg
        self.data2 = ''
        self.data3 = ''
        self.data4 = ''
        self.aesout = ''
        self.HMAC1 = ''
        self.HMAC2 = ''
  
    def __iter__(self):   
        return self   
        
    def make_pkt():
        pass

    def extract_pkt():
        pass

    def GenerateKey(self):
        '生成各类key'
        #self.aeskey = ?
        #self..
        pass

    def PacketFill(message,seq):
         '包随机填充，需保证填充后的位数为偶数，且不超过996位'
        pass

    def Re_PacketFill(message):
        pass

    def AESEncrypt(self):
        pass

    def AESDecrypt(self):
        pass

    def m_exchange(self):
        pass

    def hmac_md5():
        pass