#!/usr/bin/env python
from netsocket import communication

if __name__ == '__main__':
    com=communication.com()
    com.SendSecurity('12213123','localhost',12346)
