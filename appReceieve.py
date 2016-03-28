#!/usr/bin/env python
# -*- coding: utf-8 -*-
from netsocket import communication
if __name__ == '__main__':
    com=communication.com()
    com.ReceieveSecurity('localhost',12346)
