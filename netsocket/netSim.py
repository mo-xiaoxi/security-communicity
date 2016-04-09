#random packet drop net_sim 

import socket
import random

#program config 
n_ingress_port = 40001 #port wait for sender 
n_egress_port = 40002 #receiver port
local_addr = "127.0.0.1" 

#parameters
packet_loss_rate = 0.1 #between 0 and 1
max_packet_len = 1024


if __name__ == "__main__":
    ss = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sr = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sr.bind((local_addr, n_ingress_port))
    
    try:
        while(True):
            data, in_addr = sr.recvfrom(max_packet_len)
            if random.random() < packet_loss_rate:
                pass
                print("received packet from " + str(in_addr))
                print("dropped")
            else:
                ss.send(data, (local_addr, n_egress_port))
                print("received packet from " + str(in_addr))
                print("forwarded to " + str((local_addr, n_egress_port)))

    except KeyboardInterrupt:
        sr.close()
        ss.close()
        print("caught ctrl + d or z or c or whatever......")