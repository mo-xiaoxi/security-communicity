#!/usr/bin/python
# -*- coding: utf-8 -*-
__Author__ = 'moxiaoxi'
__Filename__ = 'testCription.py'
#coding: utf-8  
import thread  
from time import sleep, ctime  
  
def loop0():  
    print 'loop0 start at：', ctime()  
    print 'loop0挂起4秒'  
    sleep(4)  
    print 'loop0 done at：', ctime()  
  
def ReceieveSecurity(host,port):  
    print host
    print port
    print 'loop1 start at：', ctime()  
    print 'loop1挂起2秒'  
    sleep(2)  
    print 'loop1 done at：', ctime()  
  
def main():  
    print 'main thread start!'  
    thread.start_new_thread(ReceieveSecurity, ('localhost',12314))  
    thread.start_new_thread(loop0, ())  
    sleep(6)  #主线程睡眠等待子线程结束  
    print 'all done at:', ctime()  
  
if __name__ == '__main__':  
    main()  