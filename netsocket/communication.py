#!/usr/bin/python
# -*- coding: utf-8 -*-
__Author__ = 'moxiaoxi and lixu'
__Filename__ = 'communication.py'
'''
getPrintKey(str)
由于在大包时，struct.pack("<1024s32s",messagetmp,h)，messagetmp的长度往往
小于1024。此时系统会自动补足数据。因此，在解包时就会出现错误。所以，构造一个getPrintKey
函数，用于去除自动补足的数据

readFile(string,typename)
该函数主要用于读取初始化文件，用于初始化key，seq

writeFile(string,i,typename)
该函数用于向文件中写入key与seq 

class com()://信息交互类
    __init__（self) 类初始化
    def SendSecurity(self,str,host,port)    发送数据
    def ReceieveSecurity(self,host,port)    接受数据
暂时没有中文进行处理
'''

import sys
import socket
import struct 
import thread
import time  #just for test
from comlib import File,Subcontracting,aes,hmac,getNeededKey,messageExchangge,keyExpand,packetFill


#去除不可打印字符（这里主要用来去除打包时，填充的包）
def getPrintKey(str):
    import string
    printable = set(string.printable)
    return filter(lambda x:x in printable,str)

#发送信息类
class Send():
    def __init__(self):
        self.time = 2 #发包超时时间
        self.bufsiz = 544
        self.keyFile = './netsocket/s_key'
        self.key = File.readFile(self.keyFile,'key')
        self.sendSeqFile = './netsocket/s_count'
        self.seqSend = File.readFile(self.sendSeqFile,'seq')
        self.msgFile = './netsocket/msgSend'
        self.timeoutCount = 0 #超时重发次数


    def SendSecurity(self,str,host,port):
        ADDR = (host,port)#这里未加参数验证，后期需要修改，暂时不知道咋改
        #初始化socket
        try:
            Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error, msg:
            print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
            sys.exit();
        # 设置超时
        Sock.settimeout(self.time)
        #得到要发送的消息
        #message='message'
        #对message按缓冲长度分包
        datas=Subcontracting.Subcontracting(str,2)
        #这里对于断电重启，默认重启后，还是从appsend进入，这样的话，不需要读取msgfile，后期看情况修改
        File.writeFile(self.msgFile,datas,'msg')
        while self.seqSend < len(datas):
            if not datas[self.seqSend]:
                print "data error"
                break
            #包填充成 seq（8位）＋len（8位）＋data[i]＋rand(这里保证大小不大于512)
            message,lenOfData=packetFill.packetFill(datas[self.seqSend],self.seqSend)
            #使用key的中间三分之一进行aes加密（下面生成一个AES加解密器）
            AES=aes.prpcrypt(getNeededKey.getKey(self.key,1))
            #对message进行aes加密
            messagetmp=AES.encrypt(message)
            #对message进行hmac
            h = hmac.hmac_md5(getNeededKey.getKey(self.key,0), message).hexdigest()
            #得到本地ack校验值
            acktmp = messageExchangge.m_exchange(messagetmp)
            ack =  hmac.hmac_md5(getNeededKey.getKey(self.key,2), acktmp).hexdigest()
            #打包成发送数据格式 AES加密后数据（最大512位）＋HMAC输出（32位）
            data=struct.pack("<1024s32s",messagetmp,h)
            #发送数据   
            Sock.sendto(data,ADDR)
            # just for test
            # print 'origin:',datas[self.seqSend]
            # print 'packetFill:',message
            # print 'AES:',messagetmp
            # print 'HMAC:',h
            # print 'ack:',ack
            # print 'data:',data
            # print 'ADDR:',ADDR
            # print 'ackexchangge:',acktmp
            # print 'lenOfOriginData:',lenOfData
            # print self.key
            # print getNeededKey.getKey(self.key,1)
            # print 'k0',getNeededKey.getKey(self.key,0)
            # print getNeededKey.getKey(self.key,2)
            # test ending
            while True:
                try:
                    ackmessage,address = Sock.recvfrom(self.bufsiz) #接收校验包
                    if ackmessage==ack:
                        print 'ack successful ! send next packet'#验证校验包
                        self.key=keyExpand.xor_string(self.key,datas[self.seqSend])
                        self.seqSend=self.seqSend+1
                        #序列值循环
                        if self.seqSend == 0xFF:
                            self.seqSend = 1#这里存在一个循环溢出，断电后无法定位的问题！还未解决
                        print 'seq and key update successful , we save it !'
                        #保存操作
                        File.writeFile(self.sendSeqFile,self.seqSend,'seq')
                        File.writeFile(self.keyFile,self.key,'key')
                        time.sleep(1)
                        #保存操作结束
                        break
                    else:
                        print "ack data error,send again"
                        print "ackmessage receieved:   ",ackmessage
                        print "ackmessage local:   ",ack
                        Sock.sendto(data,ADDR)
                except socket.timeout:
                    print "timeout,send again"
                    Sock.sendto(data,ADDR) 
                    self.timeoutCount = self.timeoutCount + 1
                    #超时重发 这里还需要做一个多次重发，直接放弃的丢包
                    if self.timeoutCount > 10:
                        print "Failed to send successfully !something erorr ! please check the system !" 
                        sys.exit();
        print "all send done !"
        Sock.close()
        #重置序列值
        File.writeFile(self.sendSeqFile,'0','seq')
        File.resetFile(self.msgFile)
        return 1


#接受信息类
class Rec():
    def __init__(self):
        self.bufsiz = 544
        self.keyFile = './netsocket/r_key'
        self.key = File.readFile(self.keyFile,'key')
        self.recSeqFile = './netsocket/r_count'
        self.seqRec = File.readFile(self.recSeqFile,'seq')
        self.msgFile = './netsocket/msgRec'
        self.end = False

    def ReceieveSecurity(self,host,port):
        # 声明全局变量，接收消息后更改  
        #sequence
        ADDR = (host,port)#这里未加参数验证，后期需要修改，暂时不知道咋改
        # 初始化UDP socket
        try:
            ser_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error, msg:
            print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]

        ser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ser_socket.bind(ADDR)
        while not self.end:
            try:
                #接收数据，发送者地址
                message, cli_address = ser_socket.recvfrom(2048)
            except:
                traceback.print_exc()
                continue
            #解开数据包
            data,h=struct.unpack("<1024s32s",message)
            data = getPrintKey(data)
            #生成AES
            AES=aes.prpcrypt(getNeededKey.getKey(self.key,1))
            #得到本地ack校验值
            acktmp = messageExchangge.m_exchange(data)
            s_ack =  hmac.hmac_md5(getNeededKey.getKey(self.key,2), acktmp).hexdigest()
            #解密文件包
            data=AES.decrypt(data)
            #对message进行hmac
            s_h = hmac.hmac_md5(getNeededKey.getKey(self.key,0), data).hexdigest()       
            #解除填充
            tmp,i=packetFill.re_packetFill(data)
            #just for test
            #print s_h
            #print h
            #print tmp
            #print 'hello:   ',h
            #print 'k0',getNeededKey.getKey(self.key,0)
            #print 'jiemi:',data
            #print "acktemp:    ",acktmp
            #end test
            #信息正确可以处理
            if (i == (self.seqRec+1)and (s_h==h)):
                print "sequence sucessfully ,save it !"
                self.seqRec = i
                #更新密钥
                self.key=keyExpand.xor_string(self.key,tmp)
                #储存数据
                File.writeFile(self.recSeqFile,self.seqRec,'seq')
                File.writeFile(self.keyFile,self.key,'key')
                File.writeFile(self.msgFile,tmp,'msg')
                #储存结束
                ser_socket.sendto(s_ack, cli_address)#发送校验包
                print "send to ",cli_address,"data:",s_ack
                if(tmp == 'end'):
                    self.end = True
            #发送了重复的信息，那么不保存只发送hmac，让客户端更新状态
            else:#(i != (sequence+1)and (s_h==h)):
                print "sequence error,we still send ack packet to client !"
                ser_socket.sendto(s_ack, cli_address)
                print "send to ",cli_address,"data:",s_ack
        print "all receieved !"
        Rec = File.readFile(self.msgFile,'msg')
        Rec = Rec[0:len(Rec)-3]
        print "RecDATA:",Rec
        ser_socket.close()
        #重置序列值
        File.writeFile(self.recSeqFile,'-1','key')
        File.resetFile(self.msgFile)
        return 1

    def server(self,host,port):
        #通过server开一个线程，在后台监听受到的信息,后期实现
        #ReceieveSecurity
        return



if __name__ == '__main__':
    print 1
    

