#!/usr/bin/python
# -*- coding: utf-8 -*-
__Author__ = 'moxiaoxi and lixu'
__Filename__ = 'communication.py'


import sys
import socket
import struct 
import thread
import time  #just for test
from comlib import File,Cryption


#发送信息类
class Send():
    def __init__(self,host,port):
        #读取配置文件
        config = File.readFile('./netsocket/file/Send/config.json','json')
        self.keyFile = config['keyFile']
        self.msgFile = config['msgFile']
        self.SeqFile = config['SeqFile']
        self.stateFile = config['stateFile']
        self.msgFile = config['msgFile']

        self.time =config['timeout'] #发包超时时间
        self.bufsiz = config['bufsiz']
        self.key = File.readFile(self.keyFile,'key')
        self.seq = File.readFile(self.SeqFile,'num')
        self.reSendCount = config['reSendCount'] #超时重发次数
        self.state= File.readFile(self.stateFile,'num')
        self.ADDR = (str(host),int(port))
        #初始化socket
        try:
            self.Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error, msg:
            print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
            sys.exit();
        # 设置超时
        self.Sock.settimeout(self.time)

    def checkState(self):
        if(self.state==0):
            return 0#表示上次发送成功
        elif(self.state==1):
            msg=File.readFile(self.msgFile,'msg')
            if(self.SendSecurity(msg) == True):
                return 1#表示重发成功
            else:
                print 'Failed to resend last msg. please check network'
                sys.exit(2)#表示初始重发失败
                #return 2
        else:
            return -1 #表示状态码错误

    def SendSecurity(self,msg):
        File.writeFile(self.msgFile,msg,'msg')
        File.writeFile(self.stateFile,1,'state')
        packet,ack=Cryption.encrypt(msg,self.seq,self.key)
        self.Sock.sendto(packet,self.ADDR)
        while True:
            try:
                ackmessage,address = self.Sock.recvfrom(self.bufsiz) #接收校验包
                if ackmessage==ack:
                    print 'ack successful ! send next packet'#验证校验包
                    self.key=Cryption.xor_string(self.key,msg)
                    self.seq=self.seq+1
                    self.reSendCount = 0
                    #序列值循环
                    if self.seq == 0xFF:
                        self.seq = 1#这里存在一个循环溢出，断电后无法定位的问题！还未解决
                    print 'seq and key update successful , we save it !'
                    #保存操作
                    File.writeFile(self.SeqFile,self.seq,'seq')
                    File.writeFile(self.keyFile,self.key,'key')
                    File.writeFile(self.stateFile,0,'state')
                    #time.sleep(1)
                    print 'save successful !'
                    #保存操作结束
                    return True#表示发送成功
                else:
                    print "ack data error,send again"
                    print "ackmessage receieved:   ",ackmessage
                    print "ackmessage local:   ",ack
                    self.Sock.sendto(packet,self.ADDR)
                    self.reSendCount = self.reSendCount + 1
                    if self.reSendCount > 10:
                        print "Failed to send  !something erorr ! please check the system !" 
                        return False
            except socket.timeout:
                print "timeout,send again"
                self.Sock.sendto(packet,self.ADDR) 
                self.reSendCount = self.reSendCount + 1
                #超时重发 这里还需要做一个多次重发，直接放弃的丢包
                if self.reSendCount > 10:
                    print "Failed to send !something erorr ! please check the system !" 
                    return False
    def close(self):
        self.Sock.close()
        print "socket close"
        File.writeFile(self.SeqFile,'0','num')
        return 1

#接受信息类
class Rec():
    def __init__(self,host,port):
        ADDR = (host,port)#这里未加参数验证，后期需要修改，暂时不知道咋改
        # 初始化UDP socket
        try:
            self.ser_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error, msg:
            print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
        self.ser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ser_socket.bind(ADDR)

        #读取配置文件
        config = File.readFile('./netsocket/file/Rec/config.json','json')
        self.keyFile = config['keyFile']
        self.msgFile = config['msgFile']
        self.SeqFile = config['SeqFile']
        self.stateFile = config['stateFile']
        self.time = config['time']
        self.bufsiz = config['bufsiz']
        
        self.key = File.readFile(self.keyFile,'key')
        self.seqRec = File.readFile(self.SeqFile,'num')
        self.state= File.readFile(self.stateFile,'num')
        self.kn = self.key[0:48]
        self.kp = self.key[48:96]

    def checkstate(self):
        if self.state == 0 :
            print "The last time receive success"
            return 1
        elif self.state == 1 :
            try:
                ReceieveSecurity()
                self.state == 0
                print "Last time receiving failure, update the status succeed"
                return 1
            except:
                print "Last time receiving failure, update the status failed"
                return 0

    def ReceieveSecurity(self):
        try:
            #接收数据，发送者地址
            message, cli_address = self.ser_socket.recvfrom(2048)
        except:
            print "can't receieve all message !"
            traceback.print_exc()
        #将message与key生成ack和解密
        data, s_ack= Cryption.decrypt(message,self.seqRec,self.kn)
        print data
        #信息正确可以处理
        if (not(isinstance(data, bool))and data != False):
            self.seqRec =self.seqRec +1
            print "sequence sucessfully ,save it !"
            #更新密钥
            self.kp = self.kn
            self.kn = Cryption.xor_string(self.kn,data)
            self.key =self.kn + self.kp
            #print 'key',self.seqRec
            #储存数据
            File.writeFile(self.SeqFile,self.seqRec,'seq')
            File.writeFile(self.keyFile,self.key,'key')
            File.writeFile(self.msgFile,data,'msg')
            #储存结束
            self.ser_socket.sendto(s_ack, cli_address)#发送校验包
            print "send to ",cli_address,"data:",s_ack
            return data
        #发送了重复的信息，那么不保存只发送hmac，让客户端更新状态
        else:#(i != (sequence+1)and (s_h==h)):
            data, s_ack = Cryption.decrypt(message,self.seqRec,self.kp)
            print data
            if(not(isinstance(data, bool))and data != False):
                 print "hmac(now) error,hmac(pass)right ,we still send ack packet to client !"
                 self.ser_socket.sendto(s_ack, cli_address)
                 print "send to ",cli_address,"data:",s_ack
            else:
                print "hmac(now) error,hmac(pass)error!"

    def aut_close(self):
        print "receieved close !"
        self.ser_socket.close()
        #重置序列值
        File.writeFile(self.SeqFile,'-1','num')
        # File.resetFile(self.msgFile)
    def man_close(self):
        self.state == 1
        File.writeFile(self.stateFile,self.state,'key')
        self.ser_socket.close()
        


                    
if __name__ == '__main__':
    '''
    Snd = Send('127.0.0.1',12345)
    Snd.checkState()
    Snd.SendSecurity('123')
    '''

