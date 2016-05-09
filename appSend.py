#!/usr/bin/python
# -*- coding: utf-8 -*-
__Author__ = 'moxiaoxi'
__Filename__ = 'appSend.py'
from netsocket import communication
import random
if __name__ == '__main__':
    com=communication.Send('127.0.0.1',40001)
    com.checkState()
    # com.SendSecurity('1')
    # com.SendSecurity('2')
    # com.SendSecurity('3')
    # com.SendSecurity('4')
    # com.SendSecurity('5')
    # com.SendSecurity('6')
    # com.SendSecurity('7')
    # com.SendSecurity('8')
    # com.SendSecurity('9')
    # com.SendSecurity('end')
    for i in range(0,255):#发送的消息不能为0
        message=""
        length=random.randint(1,0xFF)
        message=''.join(chr(random.randint(0, 0xFF)) for i in range(100))
        com.SendSecurity(message)#这里出错，记得处理
    com.SendSecurity('end')
    com.close()
