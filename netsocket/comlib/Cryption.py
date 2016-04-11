#!/usr/bin/python
# -*- coding: utf-8 -*-
__Author__ = 'moxiaoxi and lixu '
__Filename__ = 'Cryption.py'
'''
所有加解密操作均在该文件中实现
外部只需要调用调用encrypt与decrypt函数即可。
'''
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from hashlib import md5
from itertools import cycle, izip
import struct 
import random

'''
整体包加解密函数
'''
def encrypt( msg, seq,key):
    #包填充
    msgtmp=packetFill(msg,seq)
    #使用key的中间三分之一进行aes加密（下面生成一个AES加解密器）
    aes = prpcrypt(getKey(key,1))
    #对message进行aes加密
    aesout = aes.encrypt(msgtmp)
    #对message进行hmac
    h = hmac_md5(getKey(key, 0), msgtmp).hexdigest()
    #得到本地ack校验值
    ack = hmac_md5(getKey(key, 2), m_exchange(aesout)).hexdigest()
    #打包成发送数据格式 AES加密后数据（最大512位）＋HMAC输出（32位）
    packet = struct.pack("<1024s32s", aesout, h)
    return packet, ack

def decrypt(packet, seq,key):
    try:
        aesout, h = struct.unpack("<1024s32s", packet)
    except: 
        print 'packet has wrong format !'
        return False,False
    aesout = getPrintdata(aesout)
    #生成AES
    aes = prpcrypt(getKey(key, 1))
    #得到ack返回值
    ack = hmac_md5(getKey(key, 2), m_exchange(aesout)).hexdigest()
    #解密文件包
    msgtmp = aes.decrypt(aesout)
    #对msgtmp进行hmac
    s_h = hmac_md5(getKey(key,0), msgtmp).hexdigest()
    print s_h
    print h
    if s_h == h:
        msg,m_seq= re_packetFill(msgtmp)
        if int(m_seq) == int(seq) +1:
            return msg,ack
        else:
            return False,False
    else:
        return False, False
    
'''
key为hmac密钥，msg表示传入信息
rom cryption import hmac
h = hmac.hmac_md5("key", "Im ted")
print h.hexdigest()#99f6545ceecfc05cf7751c2e6a30715d
'''


trans_5C = "".join(chr(x ^ 0x5c) for x in xrange(256))
trans_36 = "".join(chr(x ^ 0x36) for x in xrange(256))
blocksize = md5().block_size

def hmac_md5(key, msg):
  if len(key) > blocksize:
    key = md5(key).digest()
  key += chr(0) * (blocksize - len(key))
  o_key_pad = key.translate(trans_5C)
  i_key_pad = key.translate(trans_36)
  return md5(o_key_pad + md5(i_key_pad + msg).digest())



'''
每次传入message信息与key异或处理生成新的密钥_key。
然后返回_key

#test  keyExpand
k="1231231231231231"
m="m1"

>>> 
_KPTR   ZGRU\

'''


def xor_string(message, key):
    
    #message=message[0:48]
    _key = ''.join(chr((ord(c)^ord(k))) for c,k in izip(message, cycle(key)))
    # print('%s ^ %s = %s' % (message, key, cyphered))
    
    return _key


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


'''
每次传入一个message
此message必须为偶数，否则爆出异常
当为偶数时候将message一分为二前后交换顺序

#test  messageExchangge
print messageExchangge.m_exchange("abcdefsdfswerd")

>>> 
dfswerdabcdefs
'''


def m_exchange(message):
    _len=len(message)
    if (_len % 2) == 0:
        n=_len/2
        sStr1 = message [n:_len]+message [0:n]
        return sStr1
    else:
        raise "Message Not Even Number Error"




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
    return message
    
def re_packetFill(message):
    m_length=int(message[8:16])
    seq=int(message[0:8])
    message=message[16:16+m_length]
    return message,seq

'''
由于在打包时，struct.pack("<1024s32s",messagetmp,h)，messagetmp的长度往往
小于1024。此时系统会自动补足数据。因此，在解包时就会出现错误。所以，构造一个getPrintKey
函数，用于去除自动补足的数据
去除不可打印字符（这里主要用来去除打包时，填充的包）
'''
def getPrintdata(str):
    import string
    printable = set(string.printable)
    return filter(lambda x:x in printable,str)


'''
AES实现
from cryption import aes
#test aes
key = '1234567891234567'  # Store this somewhere safe
aestest = aes.prpcrypt(key)
ciphertext = aestest.encrypt('M1')
print ciphertext
plaintext = aestest.decrypt(ciphertext)
print plaintext
'''
class prpcrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC
     
    #加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        #这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        length = 16
        count = len(text)
        add = length - (count % length)
        text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        #因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        #所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)
     
    #解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')



if __name__ == "__main__":
    msg='123456'
    key='123456789123456712345678912345671234567891234567'
    c_seq='1'
    packet,c_ack = encrypt(msg,c_seq,key)
    print packet,c_ack
    s_seq='0'
    msg,s_ack = decrypt(packet,s_seq,key)
    print msg,s_ack
    # #test for aes
    # data='savaeff'
    # key='1234567891234567'
    # aes=prpcrypt(key)
    # enc=aes.encrypt(data)
    # print enc
    # dec=aes.decrypt(enc)
    # print dec
    # #test for hmac
    # h = hmac_md5("0000000100000002m2ﾻÉè5úIBÏ&þïﾎQbﾾﾋiëﾑYﾒú﾿ﾏ", "\^XZ T")
    # print h.hexdigest()
    # print len(h.hexdigest())
    # h = hmac_md5("0000000100000002m2ﾻÉè5úIBÏ&þïﾎQbﾾﾋiëﾑYﾒú﾿ﾏ", "\^XZ T")
    # print h.hexdigest()
    # print len(h.hexdigest())
    # h = hmac_md5("0000000100000002m2ﾻÉè5úIBÏ&þïﾎQbﾾﾋiëﾑYﾒú﾿ﾏ", "\^XZ T")
    # print h.hexdigest()
    # print len(h.hexdigest())
    # #test xorstring
    # k="123456789123456712345678912345671234567891234567"
    # m="m114333333333333333333333333333333333333333333"
    # enc = xor_string(m, k)
    # dec = xor_string(enc, m)
    # print len(k)
    # print len(enc)
    # print(enc)
    # print(dec)
    # #test getKey
    # key = '123456789qwertyuio'
    # for i in range(3):
    #     print getKey(key,i)
    # #test m_exchange
    # print m_exchange("abcdefsdfswerd")
    # #test packetfill
    # message='1231'
    # x=987987
    # m,y=packetFill(message,x)
    # print m,y
    # print re_packetFill(m)
