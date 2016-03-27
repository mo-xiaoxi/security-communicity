#!/usr/bin/python
# -*- coding: utf-8 -*-
__Author__ = 'lixu'
__Filename__ = 'server.py'
'''

'''
try:
    import cPickle as pickle
except ImportError:
    import pickle
    
import sys
import socket
import struct 
from cryption import aes,hmac,getNeededKey,messageExchangge,keyExpand,packetFill
import threading
from threading import Thread

import socket,hashlib
import time
import struct
import traceback

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

# 全局变量
is_ending = False
#打开计数文件
'''
host为空表示bind可以绑定到所有有效地址上
port 必须要大于1024
bufsiz为缓冲区 我们设置为1K
'''
host = 'localhost'  
port = 12345
bufsiz = 1024
ADDR = (host,port)
key='123456789123456712345678912345671234567891234567'

def getPrintKey(str):
    import string
    printable = set(string.printable)
    return filter(lambda x:x in printable,str)

# 接收线程类，用于接收客户端发送的消息
class UdpReceiver(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_stop = False
                
    def run(self):
        while not self.thread_stop:
            # 声明全局变量，接收消息后更改  
            global is_ending
            global sequence
            global key 
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
            print 'chuliqian',data
            data = getPrintKey(data)
            
            print 'chulihou',data
            print 'hmac:',h,cli_address
            print 'key',key
            AES=aes.prpcrypt(getNeededKey.getkey(key,1))
            #得到本地ack校验值
            acktmp = messageExchangge.m_exchange(data)
            s_ack =  hmac.hmac_md5(getNeededKey.getkey(key,2), acktmp).hexdigest()
            #s_ack = md5(acktmp)
            print data 
            #解密文件包
            data=AES.decrypt(data)
            #对message进行hmac
            s_h = hmac.hmac_md5(getNeededKey.getkey(key,0), data).hexdigest()
            #s_h=hmac.hmac_md5("\^XZ	T", "0000000100000002m2ﾻÉè5úIBÏ&þïﾎQbﾾﾋiëﾑYﾒú﾿ﾏ").hexdigest()
            #print 'helloooooooooooooooooooooooo:   ',h
            #print 'k0',getNeededKey.getkey(key,0)
            #print 'jiemi:',data
            #print "acktemp:    ",acktmp
            #解除填充
            tmp,i=packetFill.re_packetFill(data)
            #print 'dui bi s_h he h'
            #print s_h
            #print h
            #print tmp
            #信息正确可以处理
            if (i == (sequence+1)and (s_h==h)):
                  
                print "sequence sucessfully ,save it !"
                print tmp
                #储存数据
                f = open('output.txt', 'a')
                datas=pickle.dump(tmp,f)
                f.close()
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
                
                
            

    def stop(self):
        self.thread_stop = True



if __name__=='__main__':
    # 初始化UDP socket
    try:
        ser_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error, msg:
        print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]

    ser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ser_socket.bind(ADDR)
    #sequence = readfile('s_count.txt') #得到序列值
    sequence=-1#测试用

    receiveThread = UdpReceiver()
    receiveThread.setDaemon(True)           # 该选项设置后使得主线程退出后子线程同时退出
    receiveThread.start()#开启线程
    #便于后期扩展
    while True :
        if is_ending: 
            time.sleep(1) 
            break
        else:
            time.sleep(1)
    
    receiveThread.stop()#结束线程
    print "receiveThread ended!"
    ser_socket.close()
