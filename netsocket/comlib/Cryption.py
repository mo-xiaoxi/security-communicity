#!/usr/bin/python
# -*- coding: utf-8 -*-
__Author__ = 'moxiaoxi and lixu '
__Filename__ = 'Cryption.py'
'''
所有加解密操作均在该文件中实现
外部只需要调用调用encrypt与decrypt函数即可。
'''

from Crypto.Cipher import AES
from Crypto import Random
from binascii import b2a_hex, a2b_hex
import hmac
from itertools import cycle, izip
import struct
import random 

MAX_SEQUENCE_NUMBER=512#感觉这里还得封装成一个类，暂时没时间改
PACKET_SIZE=1024
'''
整体包加解密函数
'''
def encrypt( msg, seq,key):
    if int(seq) >= MAX_SEQUENCE_NUMBER:
        raise ValueError("Sequence Number must be smaller than {} but {} is given"
            .format(MAX_SEQUENCE_NUMBER, seq))
    #包填充
    msgtmp=packetFill(msg,seq)
    #使用key的中间三分之一进行aes加密（下面生成一个AES加解密器）
    aes = AESCipher(getKey(key,1))
    #对message进行aes加密
    aesout = aes.encrypt(msgtmp)
    #对message进行hmac
    h = hmac_md5(getKey(key, 0), msgtmp)
    #得到本地ack校验值
    ack = hmac_md5(getKey(key, 2), m_exchange(aesout))
    #打包成发送数据格式 AES加密后数据（最大1024位）＋HMAC输出（32位）
    if len(aesout) > PACKET_SIZE:
        raise ValueError("Data length should be less than of {}  but {} is given".format(PACKET_SIZE, len(aesout)))
    packet = struct.pack("<1024s32s", aesout, h)
    return packet, ack
'''
若包格式错误，直接返回packet,"format wrong",False
若hmac校验错误，返回msg,"hmac wrong",False
若seq校验错误，返回msg,"hmac wrong",False
'''
def decrypt(packet, seq,key):
    try:
        aesout, h = struct.unpack("<1024s32s", packet)
    except: 
        print 'packet has wrong format !'
        return packet,"format wrong",False
    aesout = getPrintdata(aesout)
    #生成AES
    aes = AESCipher(getKey(key, 1))
    #得到ack返回值
    ack = hmac_md5(getKey(key, 2), m_exchange(aesout))
    #解密文件包
    msgtmp = aes.decrypt(aesout)
    #对msgtmp进行hmac
    s_h = hmac_md5(getKey(key,0), msgtmp)
    if s_h == h:
        msg,m_seq= re_packetFill(msgtmp)
        if int(m_seq) == (int(seq) +1)%0xFF:
            return msg,ack,True
        else:
            return msg,"seq wrong",False
    else:
        return msgtmp,"hmac wrong",False
    
'''
key为hmac密钥，msg表示传入信息
'''

def hmac_md5(key, msg):
    myhmac = hmac.new(bytes(key))
    myhmac.update(bytes(msg))
    return myhmac.hexdigest()

'''
每次传入message信息与key异或处理生成新的密钥_key。
然后返回_key
'''
def keyExpand(key,message):
    #message=message[0:48]
    l=len(key)
    key.decode("hex")
    _key = ''.join(chr((ord(c)^ord(k))) for c,k in izip(key, cycle(message)))
    # print('%s ^ %s = %s' % (message, key, cyphered))
    return _key.encode("hex")[:l]


'''
当i＝0时，取key前三分之一
当i＝1时，取key中间三分之一
当i＝2时，取key后三分之一
当i不为上述情况或者i和key类型不符合时，raise 输入参数错误
'''
def getKey(key,i):
    l=len(key)
    if  isinstance(key,str) and isinstance(i,int) and l%3 == 0 :
        l/=3
        if(i==0):
            return key[0:l]
        elif(i==1):
            return key[0:2*l]
        elif(i==2):
            return key[3*l:4*l]
        else:
            raise ValueError('2the  argument not allowed')
    else:
        raise ValueError('1the  argument not allowed')


'''
每次传入一个message
此message必须为偶数，否则爆出异常
当为偶数时候将message一分为二前后交换顺序
'''
def m_exchange(message):
    _len=len(message)
    if (_len % 2) == 0:
        n=_len/2
        sStr1 = message [n:_len]+message [0:n]
        return sStr1
    else:
        raise "Message Not Even Number , Error!"

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
'''

class AESCipher:
    def __init__( self, key ):
        """
        Requires hex encoded param as a key
        """
        self.key = key.decode("hex")

    def encrypt( self, raw ):
        """
        Returns hex encoded encrypted value!
        """
        iv = Random.new().read(AES.block_size);
        cipher = AES.new( self.key, AES.MODE_CFB, iv )
        return ( iv + cipher.encrypt( raw ) ).encode("hex")

    def decrypt( self, enc ):
        """
        Requires hex encoded param to decrypt
        """
        enc = enc.decode("hex")
        iv = enc[:16]
        enc= enc[16:]
        cipher = AES.new(self.key, AES.MODE_CFB, iv )
        return cipher.decrypt( enc)
     



if __name__ == "__main__":
    msg='123456'
    key='123456789123456712345678912345671234567891234567123456789123456712345678912345671234567891234567'
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
