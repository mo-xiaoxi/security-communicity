#!/usr/bin/python
# -*- coding: utf-8 -*-
__Author__ = 'moxiaoxi'
__Filename__ = 'testCription.py'
'''

'''
import socket

class com():
    def __init__(self,host,port):
        self.ADDR = (host,port)#这里未加参数验证，后期需要修改，暂时不知道咋改
        self.time = 5
        self.bufsiz = 1024
        self.key='first key'
    def SendSecurity(str,host,port):
        #初始化socket
        try:
            Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error, msg:
            print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
        sys.exit();
        # 设置超时
        Sock.settimeout(time)

        datas=['m1','m2','m3']
        
        Sock.close()