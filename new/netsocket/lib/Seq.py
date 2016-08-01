#!/usr/bin/env python
# -*- coding:utf-8 -*-

MAXSEQ = 2**8-1
MINSEQ = 0
class Seq(object):
    def __init__(self,base,window):
        if(base > MAXSEQ||base < MINSEQ):
            raise ValueError("Seq init error ! start {}  end  {}".format(MINSEQ, MAXSEQ))  
        self.base = base  
        self.window = window

    def __iter__(self):
        return self


    def next(self):
        r = self.n
        if self.n < self.end:   
            self.n = self.n + 1     
        else:
            self.n = self.start    
        return r

    def CheckinWindow(self,seq):
        pass