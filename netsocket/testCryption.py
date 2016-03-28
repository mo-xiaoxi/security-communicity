#!/usr/bin/python
# -*- coding: utf-8 -*-
__Author__ = 'moxiaoxi'
__Filename__ = 'testCription.py'
from comlib import File
print "before :"
print 'r_key:',File.readFile('r_key','key')
print 's_key:',File.readFile('s_key','key')
print 'r_count:',File.readFile('r_count','seq')
print 's_count:',File.readFile('s_count','seq')
print 'msgRec:',File.readFile('msgRec','msg')
print 'msgSend:',File.readFile('msgSend','msg')
File.writeFile('r_key','123456789123456712345678912345671234567891234567','key')
File.writeFile('s_key','123456789123456712345678912345671234567891234567','key')
File.writeFile('r_count','-1','seq')
File.writeFile('s_count','0','seq')
File.resetFile('msgSend')
File.resetFile('msgRec')
print "after:"
print 'r_key:',File.readFile('r_key','key')
print 's_key:',File.readFile('s_key','key')
print 'r_count:',File.readFile('r_count','seq')
print 's_count:',File.readFile('s_count','seq')
print 'msgRec:',File.readFile('msgRec','msg')
print 'msgSend:',File.readFile('msgSend','msg')

