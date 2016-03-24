#!/usr/bin/env python
# -*- coding:utf-8 -*-
#__Author__ = moxiaoxi
#___name___ = task2 as server(Bob)

#两个模块来实现序列化


try:
    import cPickle as pickle
except ImportError:
    import pickle   
import socket,hashlib
import time
import struct
from threading import Thread
import traceback
import threading
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import sys

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
port = 23457
bufsiz = 1024
ADDR = (host,port)
k="1231231231231231"
Dec=prpcrypt(k)




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

            try:
                message, cli_address = ser_socket.recvfrom(2048)#接收数据，发送者地址
                print "receieving data :",message#打印接收数据额
            except:
                traceback.print_exc()
                continue
            print message,cli_address
            data,i=struct.unpack("<32si",message)
            tmp=Dec.decrypt(data)

            if i == (sequence+1):
                print "sequence sucessfully ,save it !"
                #储存数据
                f = open('output.txt', 'a')
                datas=pickle.dump(tmp,f)
                f.close()
                sequence = i
                #储存计数
                with open('s_count.txt', 'w') as d:
                    d.write(str(sequence))
                
                if tmp == "end":
                    is_ending = True
                md=md5(message)
                ser_socket.sendto(md, cli_address)#发送校验包
                print "send to ",cli_address,"data:",md                
            else:
                print "sequence error,but we still send ack packet to client !"
                md=md5(message)
                ser_socket.sendto(md, cli_address)
                print "send to ",cli_address,"data:",md
                
            

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
    sequence = readfile('s_count.txt') #得到序列值

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
