#!/usr/bin/env python
from itertools import cycle, izip
from netsocket import communication

if __name__ == '__main__':
    communication.SendSecurity('123','localhost',12345)
