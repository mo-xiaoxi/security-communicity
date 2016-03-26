#!/usr/bin/python
# -*- coding: utf-8 -*-
__Author__ = 'moxiaoxi'
__Filename__ = 'testCription.py'
'''

'''
import sys
import socket
import struct 
from cryption import aes,hmac,getNeededKey,messageExchangge,keyExpand,packetFill



def SendSecurity(str,host,port):
    ADDR = (host,port)#这里未加参数验证，后期需要修改，暂时不知道咋改
    time = 5
    bufsiz = 544
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
        print 'origin:',datas[i]
        #包填充成 seq（8位）＋len（8位）＋data[i]＋rand(这里保证大小不大于512)
        message,lenOfData=packetFill.packetFill(datas[i],i)
        print 'packetFill:',message

        #使用key的中间三分之一进行aes加密（下面生成一个AES加解密器）
        AES=aes.prpcrypt(getNeededKey.getkey(key,1))
        #对message进行aes加密
        messagetmp=AES.encrypt(message)
        #对message进行hmac
        h = hmac.hmac_md5(getNeededKey.getkey(key,0), message).hexdigest()
        #得到本地ack校验值
        acktmp = messageExchangge.m_exchange(messagetmp)
        ack =  hmac.hmac_md5(getNeededKey.getkey(key,2), acktmp).hexdigest()
        #打包成发送数据格式 AES加密后数据（最大512位）＋HMAC输出（32位）
        data=struct.pack("<512s32s",messagetmp,h)
        #发送数据   
        Sock.sendto(data,ADDR)
        #just for test
        

        # print 'AES:',messagetmp
        # print 'HMAC:',h
        # print 'ack:',ack
        # print 'data:',data
        # print 'ADDR:',ADDR
        # print 'ackexchangge:',acktmp
        # print 'lenOfOriginData:',lenOfData
        # print key
        # print getNeededKey.getkey(key,1)
        # print getNeededKey.getkey(key,0)
        # print getNeededKey.getkey(key,2)
        #test ending
        while True:
            try:
                ackmessage,address = Sock.recvfrom(bufsiz) #接收校验包
                if ackmessage==ack:
                    print 'ack successful ! send next packet'#验证校验包
                    i=i+1
                    '''
                    with open('count.txt', 'w') as d:
                            d.write(str(i))
                    '''
                    print i
                    break
                else:
                    print "ack data error,send again"
                    Sock.sendto(data,ADDR)
            except socket.timeout:
                print "timeout,send again"
                Sock.sendto(data,ADDR)  #超时重发 这里还需要做一个多次重发，直接放弃的丢包 
    #senddatas(datas)
    Sock.close()
    return 1
def ReceieveSecurity(str):
    return
def server():
    #通过server开一个线程，在后台监听受到的信息
    return



if __name__ == '__main__':
    message='1231'
    x=987987
    m,y=packetFill.packetFill(message,x)
    print m,y
    SendSecurity('123','localhost',123)