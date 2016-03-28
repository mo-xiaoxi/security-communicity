#!/usr/bin/env python
from netsocket import communication

if __name__ == '__main__':
    com=communication.Send()
    com.SendSecurity('1221312qweqweqw','localhost',12340)
