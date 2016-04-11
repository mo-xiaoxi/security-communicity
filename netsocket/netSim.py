#!/usr/bin/python
# -*- coding: utf-8 -*-
#random packet drop net_sim 

import socket
import random

#program config 
n_ingress_port = 40001 #port wait for sender 
n_egress_port = 40003 #receiver port
local_addr = "127.0.0.1" 

#parameters
packet_loss_rate = 0.1 #between 0 and 1
max_packet_len = 2048


if __name__ == "__main__":
    ss = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sr = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sr.bind((local_addr, n_ingress_port))
    
    try:
        while(True):
            data_send, addr_send = sr.recvfrom(max_packet_len)
            # if random.random() < packet_loss_rate:
            #     pass
            #     print("received packet from send:" + str(addr_send))
            #     print 'data:',data_send
            #     print("dropped")
            # else:
            ss.sendto(data_send, (local_addr, n_egress_port))
            print("received packet from send:" + str(addr_send))
            print 'data:',data_send
            print("forwarded to Rec:" + str((local_addr, n_egress_port)))

            data_Rec, addr_Rec = ss.recvfrom(max_packet_len)
            # if random.random() < packet_loss_rate:
            #     pass
            #     print("received packet from Rec:" + str(addr_Rec))
            #     print 'data:',data_Rec
            #     print("dropped")
            # else:
            sr.sendto(data_Rec, (local_addr, n_ingress_port ))
            print("received packet from Rec:" + str(addr_Rec))
            print 'data:',data_Rec
            print("forwarded to send:" + str((local_addr, n_ingress_port)))

    except KeyboardInterrupt:
        sr.close()
        ss.close()
        print("caught ctrl + d or z or c or whatever......")