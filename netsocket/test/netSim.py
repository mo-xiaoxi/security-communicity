#!/usr/bin/python
# -*- coding: utf-8 -*-
__Author__ = 'moxiaoxi'
__Filename__ = 'netSim.py'

'''
用于网络测试，该版本测试代码只能线性测试代码，即必须先接受发送者发来的packet，
再转发给接受者，然后接受接受者发来的ack，最后转发给发送者。期间，过程测试代码不
接受发送者重发的数据
'''
import socket
import random

#config
RecforSender = 40000 #接受来自发送者数据的端口。
RecforReCer = None #接受来自接受者ack数据的端口  （未使用）
ForwardtoRecer = 40002 #转发给接受者，即接受者监听的端口
ForwardtoSender = None #转发给发送者的端口
local_addr = "127.0.0.1" 

#parameters
packet_loss_rate = 0.1 #between 0 and 1
packet_change_rate =0.2
max_packet_len = 1056
out_addr = None
time = 1

if __name__ == "__main__":
    RecSender = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#接受发送者发来数据的socket
    ForwardtoRec = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#转发发送者数据到接受者的socket
    ForwardtoSend = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#转发接受者数据到发送者
    RecSender.bind((local_addr, RecforSender))
    ForwardtoRec.settimeout(time)
    try:
        while(True):
            packet, in_addr = RecSender.recvfrom(max_packet_len)
            print("received packet from sender: " + str(in_addr))
            #print "packet :",packet
            if random.random() < packet_loss_rate:
                pass
                print("0ops ! packet dropped")#用于仿真sender---packet---->>receiever丢包
            else:
                if(random.random() < packet_change_rate):
                    print(" 0ops ! packet changged")#用于仿真sender---packet---->>receiever数据被篡改或数据传输时数据错误
                    packet='error packet'
                ForwardtoSender = in_addr[1]#得到发送者，发送使用的端口(不用if none判定是因为如果发送端挂了，下一次起来的发送端口会改变)
                out_addr =(local_addr,ForwardtoRecer)  
                ForwardtoRec.sendto(packet, out_addr)#转发数据给接受者
                print("forwarded to receiver:" + str(out_addr))
                try:
                    ack, in_addr = ForwardtoRec.recvfrom(max_packet_len)#得到接受者返回的ack
                    print("received ack from receiver:" + str(in_addr))
                    #print "ack :",ack
                    if random.random() < packet_loss_rate:
                        pass
                        print("0ops ! ack dropped")#用于仿真receiever---ack----->>sender丢包
                    else:
                        if(random.random() < packet_change_rate):
                            print(" 0ops ! ack changged")#用于仿真receiever---ack----->>sender数据出错
                            packet='error packet'
                        out_addr =(local_addr,ForwardtoSender)  
                        ForwardtoSend.sendto(ack, out_addr)#转发数据给发送者
                        print("forwarded to sender:" + str(out_addr))
                except socket.timeout:#这里是因为如果发送的是错误的packet给接受者，接受者不会回复任何数据，因此需要让netdsim返回到接受sender重发包的状态
                    print "we can't receive anything from receiver in time. so, we think last packet lost!"

    except KeyboardInterrupt:
        RecSender.close()
        ForwardtoRec.close()
        ForwardtoSend.close()
        print("caught ctrl + d or z or c or whatever......")