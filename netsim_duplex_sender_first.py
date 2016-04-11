#random packet drop net_sim 
#first packet must come from sender
#cannot be reused across experiments
#sender and receiver must keep the sending port unchanged throughout the experiment

import socket
import random

#program config 
n_ingress_port = 40000 #port wait for packets
n_egress_port_sender = 40001 #sender port to receive ACK  
n_egress_port_receiver = 40002 #receiver port to receive packet
n_in_port_sender = None
n_in_port_receiver = None
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
                if n_in_port_sender == None:
                    n_in_port_sender = in_addr[1]
                elif in_addr[1] != n_in_port_sender and n_in_port_receiver == None:
                    n_in_port_receiver = in_addr[1]
                else:
                    pass
                
                if in_addr == n_in_port_sender:
                    out_addr = (local_addr, n_egress_port_receiver)
                elif in_addr == n_in_port_receiver:
                    out_addr = (local_addr, n_egress_port_sender)
                else:
                    pass
                    
                ss.send(data, out_addr)
                print("received packet from " + str(in_addr))
                print("forwarded to " + str(out_addr))

    except KeyboardInterrupt:
        sr.close()
        ss.close()
        print("caught ctrl + d or z or c or whatever......")