#!/usr/bin/python
# -*- coding: utf-8 -*-
__Author__ = 'moxiaoxi'
__Filename__ = 'testCription.py'
from comlib import Cryption
import random
while(True):
    length=random.randint(1,50)
    msg1=''.join(chr(random.randint(0, 0xFF)) for i in range(100))
    key="123456789123456712345678912345671234567891234567"
    hmackey='1234567891234567'
    seq=2
    aesout=''
    # packet,ack,aesout=Cryption.encrypt( msg1, seq,key)
    # msg2,ack,flag=Cryption.decrypt(packet, seq-1,key,aesout)
    # if(msg1==msg2):
    #     print "nice job!"
    #     print "msg1",msg1
    #     print "msg2",msg2
    # else:
    #     print "error"
    #     print "msg1",msg1
    #     print "msg2",msg2
    #     break
    key=Cryption.getKey(key,1)
    aes1=Cryption.AESCipher('140b41b22a29bab4061bda66b6747e14')
    aes2=Cryption.AESCipher('140b41b22a29beb4061bda66b6747e14')
    aesout = aes1.encrypt(msg1)
    msg2 = aes2.decrypt(aesout)
    if(msg1!=msg2):
        print "error"
        print aesout
        print msg1
        print msg2
        print len(msg1)
        print len(msg2)
        print type(msg1)
        print type(msg2) 
        break
    # ack1=Cryption.hmac_md5(hmackey,msg1)
    # ack2=Cryption.hmac_md5(hmackey,msg1)
    # if(ack1!=ack2):
    #     print "hmackey",hmackey
    #     print "msg1",msg1
    #     print "ack1",ack1
    #     print "ack2",ack2
    #     break
# from comlib import File
# print "before :"
# print 'r_key:',File.readFile('./file/Rec/key','key')
# print 's_key:',File.readFile('./file/Send/key','key')
# print 'r_count:',File.readFile('./file/Rec/seq','num')
# print 's_count:',File.readFile('./file/Send/seq','num')
# print 'msgRec:',File.readFile('./file/Rec/msg','msg')
# print 'msgSend:',File.readFile('./file/Send/msg','msg')
# print 'configRec:',File.readFile('./file/Rec/config.json','json')
# print 'configSend:',File.readFile('./file/Send/config.json','json')
# print 'stateRec:',File.readFile('./file/Rec/state','num')
# print 'stateSend:',File.readFile('./file/Send/state','num')
# File.writeFile('./file/Rec/key','123456789123456712345678912345671234567891234567123456789123456712345678912345671234567891234567','key')
# File.writeFile('./file/Send/key','123456789123456712345678912345671234567891234567','key')
# File.writeFile('./file/Rec/seq','-1','seq')
# File.writeFile('./file/Send/seq','0','seq')
# File.resetFile('./file/Rec/msg')
# File.resetFile('./file/Send/msg')
# File.writeFile('./file/Rec/state',0,'num')
# File.writeFile('./file/Send/state',0,'num')
# print "after:"
# print 'r_key:',File.readFile('./file/Rec/key','key')
# print 's_key:',File.readFile('./file/Send/key','key')
# print 'r_count:',File.readFile('./file/Rec/seq','num')
# print 's_count:',File.readFile('./file/Send/seq','num')
# print 'msgRec:',File.readFile('./file/Rec/msg','msg')
# print 'msgSend:',File.readFile('./file/Send/msg','msg')
# print 'configRec:',File.readFile('./file/Rec/config.json','json')
# print 'configSend:',File.readFile('./file/Send/config.json','json')
# print 'stateRec:',File.readFile('./file/Rec/state','num')
# print 'stateSend:',File.readFile('./file/Send/state','num')
