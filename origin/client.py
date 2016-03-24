#!/usr/bin/python
# -*- coding: utf-8 -*-
#__Author__ = moxiaoxi
#___name___ = task2 as client(Alice)

#两个模块来实现序列化
try:
    import cPickle as pickle
except ImportError:
    import pickle
    
import socket,hashlib
import time
import struct
from  sys import exit
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
 
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



def keyexpand(k,i):
    return md5(k|datas[i])

#md5加密
def md5(str):
    import hashlib
    import types
    if type(str) is types.StringType:
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()
    else:
        return ''

def readfile(string):
    try:
        import cPickle as pickle
    except ImportError:
        import pickle
    if isinstance(string,str):
        with open(string,'rb') as d:
            i=d.read()
        i=int(i)
        return i
    else:
        return -1



host = 'localhost'
port = 23457
bufsiz = 1024
ADDR = (host,port)
time = 5
k="1231231231231231"


#初始化socket
try:
    Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();

# 设置超时
Sock.settimeout(time)

#文件读取，获取需要发送的数据
f = open('input.txt', 'rb')
datas= pickle.load(f)
f.close()
print datas

i=readfile('count.txt')


'''
向服务器发送消息，并判断接收时是否超时，若超时则重发
打包一个序列值，保证每个包的唯一性，同时也可以防止由于
传输时间过长，导致client假阳性误报server没有接受当前
包，重传问题
'''


#print len(datas)
#for i  in range(len(datas)):
while i<len(datas):
    print i
    if not datas[i]:
        print "data error"
        break
    global k
    Enc=prpcrypt(k)
    tmp=Enc.encrypt(str(datas[i]))
    data=struct.pack("<32si",tmp,i)       #打包
    Sock.sendto(data,ADDR)                   #发包
    print 'data',data,'sended ,destination',ADDR
    md=md5(data)
    print md
    while True:
        try:
            message,address = Sock.recvfrom(bufsiz) #接收校验包
            if message==md:
                print 'ack successful ! send next packet'#验证校验包
                i=i+1
                with open('count.txt', 'w') as d:
                        d.write(str(i))
                print i
                break
            else:
                print "ack data error,send again"
                Sock.sendto(data,ADDR)
        except socket.timeout:

            print "timeout,send again"
            Sock.sendto(data,ADDR)  #超时重发



Sock.close()
