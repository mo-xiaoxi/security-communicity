#!/usr/bin/env python
# -*- coding: utf-8 -*-
from netsocket import communication
if __name__ == '__main__':
    com=communication.Rec('localhost',12345)
    com.checkstate()
    while (str != 'end'):
        str=com.ReceieveSecurity()
    com.aut_close()
