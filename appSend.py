#!/usr/bin/python
# -*- coding: utf-8 -*-
__Author__ = 'moxiaoxi'
__Filename__ = 'appSend.py'
from netsocket import communication,test_time
import random
NUM=50
LENGTH=16
if __name__ == '__main__':
    com=communication.Send('127.0.0.1',40000)
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
    t = test_time.Timer()
    t.start()
    for i in range(1,NUM):#发送的消息不能为0
        message=""
        #length=random.randint(1,0xFF)
        length=LENGTH
        message=''.join(chr(random.randint(0, 0xFF)) for i in range(100))
        com.SendSecurity(message)#这里出错，记得处理
    com.SendSecurity('end')
    com.close()
    t.stop()
    print('time',t.elapsed)
    throughput=NUM*LENGTH*8/t.elapsed
    print('Throughput=NUM/t.elapsed',throughput)