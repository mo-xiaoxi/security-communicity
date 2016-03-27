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
import thread





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
    datas=['m1','m2','m3','12312','312','3','13','1','321','3','123','12','312']
    #i=readfile('count.txt')//从文件中读取初始序列号
    i=0#测试用
    while i < len(datas):
        if not datas[i]:
            print "data error"
            break

        #包填充成 seq（8位）＋len（8位）＋data[i]＋rand(这里保证大小不大于512)
        message,lenOfData=packetFill.packetFill(datas[i],i)


        #使用key的中间三分之一进行aes加密（下面生成一个AES加解密器）
        AES=aes.prpcrypt(getNeededKey.getkey(key,1))
        #对message进行aes加密
        messagetmp=AES.encrypt(message)
        #对message进行hmac
        h = hmac.hmac_md5(getNeededKey.getkey(key,0), message).hexdigest()
        #h=hmac.hmac_md5("\^XZ   T", "0000000100000002m2ﾻÉè5úIBÏ&þïﾎQbﾾﾋiëﾑYﾒú﾿ﾏ").hexdigest()
        #print 'helloooooooooooooooooooooooo:   ',h
        #得到本地ack校验值
        acktmp = messageExchangge.m_exchange(messagetmp)
        #print "acktemp:    ",acktmp
        ack =  hmac.hmac_md5(getNeededKey.getkey(key,2), acktmp).hexdigest()
        #ack = md5(acktmp)
        #打包成发送数据格式 AES加密后数据（最大512位）＋HMAC输出（32位）
        data=struct.pack("<1024s32s",messagetmp,h)
        #发送数据   
        Sock.sendto(data,ADDR)
        #just for test
        # print 'origin:',datas[i]
        print 'packetFill:',message
        print 'AES:',messagetmp
        print 'HMAC:',h
        # print 'ack:',ack
        print 'data:',data
        # print 'ADDR:',ADDR
        # print 'ackexchangge:',acktmp
        # print 'lenOfOriginData:',lenOfData
        # print key
        # print getNeededKey.getkey(key,1)
        #print 'k0',getNeededKey.getkey(key,0)
        # print getNeededKey.getkey(key,2)
        #test ending
        while True:
            try:
                ackmessage,address = Sock.recvfrom(bufsiz) #接收校验包
                if ackmessage==ack:
                    key=keyExpand.xor_string(key,datas[i])
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
                    print "ackmessage receieved:   ",ackmessage
                    print "ackmessage local:   ",ack
                    Sock.sendto(data,ADDR)
            except socket.timeout:
                print "timeout,send again"
                Sock.sendto(data,ADDR)  #超时重发 这里还需要做一个多次重发，直接放弃的丢包 
    #senddatas(datas)
    Sock.close()
    return 1

def ReceieveSecurity():
    print '12312312'
    sleep(2)  
    return

def server(host,port):
    try:
        thread.start_new_thread(ReceieveSecurity, ())  
    except:
        print "Error: unable to start thread"
    #通过server开一个线程，在后台监听受到的信息
    #ReceieveSecurity
    return



if __name__ == '__main__':
    #SendSecurity('123','localhost',12345)
    server('localhost',123456)

