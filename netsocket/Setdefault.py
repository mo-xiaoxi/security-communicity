#!/usr/bin/python
# -*- coding: utf-8 -*-
__Author__ = 'moxiaoxi'
__Filename__ = 'testCription.py'

from comlib import File
print "before :"
print 'r_key:',File.readFile('./file/Rec/key','key')
print 's_key:',File.readFile('./file/Send/key','key')
print 'r_count:',File.readFile('./file/Rec/seq','num')
print 's_count:',File.readFile('./file/Send/seq','num')
print 'msgRec:',File.readFile('./file/Rec/msg','msg')
print 'msgSend:',File.readFile('./file/Send/msg','msg')
print 'configRec:',File.readFile('./file/Rec/config.json','json')
print 'configSend:',File.readFile('./file/Send/config.json','json')
print 'stateRec:',File.readFile('./file/Rec/state','num')
print 'stateSend:',File.readFile('./file/Send/state','num')
File.writeFile('./file/Rec/key','123456789123456712345678912345671234567891234567123456789123456712345678912345671234567891234567','key')
File.writeFile('./file/Send/key','123456789123456712345678912345671234567891234567','key')
File.writeFile('./file/Rec/seq','-1','seq')
File.writeFile('./file/Send/seq','0','seq')
File.resetFile('./file/Rec/msg')
File.resetFile('./file/Send/msg')
File.writeFile('./file/Rec/state',0,'num')
File.writeFile('./file/Send/state',0,'num')
print "after:"
print 'r_key:',File.readFile('./file/Rec/key','key')
print 's_key:',File.readFile('./file/Send/key','key')
print 'r_count:',File.readFile('./file/Rec/seq','num')
print 's_count:',File.readFile('./file/Send/seq','num')
print 'msgRec:',File.readFile('./file/Rec/msg','msg')
print 'msgSend:',File.readFile('./file/Send/msg','msg')
print 'configRec:',File.readFile('./file/Rec/config.json','json')
print 'configSend:',File.readFile('./file/Send/config.json','json')
print 'stateRec:',File.readFile('./file/Rec/state','num')
print 'stateSend:',File.readFile('./file/Send/state','num')
