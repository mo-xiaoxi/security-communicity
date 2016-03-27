#!/usr/bin/python
# -*- coding: utf-8 -*-
__Author__ = 'moxiaoxi and lixu'
__Filename__ = 'communication.py'
'''

'''
import sys
import socket
import struct 
import thread
from time import sleep, ctime  
from cryption import aes,hmac,getNeededKey,messageExchangge,keyExpand,packetFill

time = 5
bufsiz = 1024
key = '123456789123456712345678912345671234567891234567'
def init():
    time = 5
    bufsiz = 544
    key='123456789123456712345678912345671234567891234567'


def getPrintKey(str):
    import string
    printable = set(string.printable)
    return filter(lambda x:x in printable,str)

def SendSecurity(str,host,port):
    ADDR = (host,port)#这里未加参数验证，后期需要修改，暂时不知道咋改
    global time
    global bufsiz
    global key
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
        #得到本地ack校验值
        acktmp = messageExchangge.m_exchange(messagetmp)
        ack =  hmac.hmac_md5(getNeededKey.getkey(key,2), acktmp).hexdigest()
        #打包成发送数据格式 AES加密后数据（最大512位）＋HMAC输出（32位）
        data=struct.pack("<1024s32s",messagetmp,h)
        #发送数据   
        Sock.sendto(data,ADDR)
        # just for test
        # print 'origin:',datas[i]
        # print 'packetFill:',message
        # print 'AES:',messagetmp
        # print 'HMAC:',h
        # print 'ack:',ack
        # print 'data:',data
        # print 'ADDR:',ADDR
        # print 'ackexchangge:',acktmp
        # print 'lenOfOriginData:',lenOfData
        # print key
        # print getNeededKey.getkey(key,1)
        # print 'k0',getNeededKey.getkey(key,0)
        # print getNeededKey.getkey(key,2)
        # test ending
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

def ReceieveSecurity(host,port):
    # 声明全局变量，接收消息后更改  
    is_ending=False
    #sequence
    global key
    ADDR = (host,port)#这里未加参数验证，后期需要修改，暂时不知道咋改
    # 初始化UDP socket
    try:
        ser_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error, msg:
        print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]

    ser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ser_socket.bind(ADDR)
    #sequence = readfile('s_count.txt') #得到序列值
    sequence=-1#测试用
    while (1):
        try:
            #接收数据，发送者地址
            message, cli_address = ser_socket.recvfrom(2048)
            #打印接收数据项
            print "receieving data :",message
        except:
            traceback.print_exc()
            continue
        #解开数据包
        data,h=struct.unpack("<1024s32s",message)
        #print 'chuliqian:',data
        data = getPrintKey(data)
        #print 'chulihou:',data
        #print 'hmac:',h,cli_address
        #print 'key',key
        AES=aes.prpcrypt(getNeededKey.getkey(key,1))
        #得到本地ack校验值
        acktmp = messageExchangge.m_exchange(data)
        s_ack =  hmac.hmac_md5(getNeededKey.getkey(key,2), acktmp).hexdigest()
        #print data 
        #解密文件包
        data=AES.decrypt(data)
        #对message进行hmac
        s_h = hmac.hmac_md5(getNeededKey.getkey(key,0), data).hexdigest()       
        #解除填充
        tmp,i=packetFill.re_packetFill(data)
        #print 'dui bi s_h he h'
        #print s_h
        #print h
        #print tmp
        #print 'hello:   ',h
        #print 'k0',getNeededKey.getkey(key,0)
        #print 'jiemi:',data
        #print "acktemp:    ",acktmp
        #信息正确可以处理
        if (i == (sequence+1)and (s_h==h)):
            print "sequence sucessfully ,save it !"
            print tmp
            #储存数据
            '''f = open('output.txt', 'a')
            datas=pickle.dump(tmp,f)
            f.close()
            '''
            sequence = i
            #更新密钥
            key=keyExpand.xor_string(key,tmp)
            #储存计数
            with open('s_count.txt', 'w') as d:
                d.write(str(sequence)) 
            if tmp == "end":
                is_ending = True
            ser_socket.sendto(s_ack, cli_address)#发送校验包
            print "send to ",cli_address,"data:",s_ack
        #发送了重复的信息，那么不保存只发送hmac，让客户端更新状态
        else:#(i != (sequence+1)and (s_h==h)):
            print "sequence error,we still send ack packet to client !"
            ser_socket.sendto(s_ack, cli_address)
            print "send to ",cli_address,"data:",s_ack
        #其余情况不做处理，让客户端超时重发
        #else:
        #   print 'hmc error,we do not sent ack and wait clint sent again' 
    return 1

def server(host,port):
    try:
        thread.start_new_thread(ReceieveSecurity, (host,port))  
    except:
        print "Error: unable to start thread"
    #通过server开一个线程，在后台监听受到的信息
    #ReceieveSecurity
    return



if __name__ == '__main__':
   #SendSecurity('123','localhost',12345)
    server('localhost',12345)

