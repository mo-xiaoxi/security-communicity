#!/usr/bin/env python
# -*- coding: utf-8 -*-
from netsocket import communication
import socket
if __name__ == '__main__':
    # try:
    #     ser_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # except socket.error, msg:
    #     print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    # ser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # ADDR=('127.0.0.1',40002)
    # ser_socket.bind(ADDR)
    # while(True):
    #     message, cli_address = ser_socket.recvfrom(2048)
    #     ser_socket.sendto('s_ack', ('127.0.0.1',40000))

    com=communication.Rec('localhost',40001)
    com.checkstate()
    while(True):
        msg=com.ReceieveSecurity()
        if(msg=='end'):
            break
    com.aut_close()
