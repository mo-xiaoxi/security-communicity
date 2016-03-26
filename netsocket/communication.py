#!/usr/bin/python
# -*- coding: utf-8 -*-
__Author__ = 'moxiaoxi'
__Filename__ = 'testCription.py'
'''

'''
import socket
from cryption import aes,hmac,getNeededKey,messageExchangge,keyExpand,packetFill



def SendSecurity(str,host,port):
    ADDR = (host,port)#这里未加参数验证，后期需要修改，暂时不知道咋改
    time = 5
    bufsiz = 1024
    key='123456789123456712345678912345671234567891234567'
    #初始化socket
    try:
        Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error, msg:
        print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();
    # 设置超时
    Sock.settimeout(time)
    #得到要发送的消息
    #message='message'
    #对message按缓冲长度分包
    datas=['m1','m2','m3']
    #i=readfile('count.txt')//从文件中读取初始序列号
    i=0#测试用
    while i < len(datas):
        if not datas[i]:
            print "data error"
            break
        AES=aes.prpcrypt(getNeededKey.getKey(key,1))
        #Sock.sendto(data,ADDR)  
    #senddatas(datas)
    Sock.close()
def ReceieveSecurity(str):
    return