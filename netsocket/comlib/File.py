#!/usr/bin/python
# -*- coding: utf-8 -*-
__Author__ = 'moxiaoxi'
__Filename__ = 'File.py'
'''
该文件后期需要修改，对应于各类读取方式，有通用解
各类文件读取，存取，重置。
该函数暂考虑，序列值的读取、key的读取、消息的读取
其参数依次为seq，key，msg
it's easy to use it !
please enjoy it !
'''
#读取文件(得到序列)
def readFile(string,typename):
    with open(string,'rb') as d:
        if(typename == 'num'):
            data=d.read()
            data=int(data)
        elif(typename == 'key'):
            data=d.read()
        elif(typename ==  'msg'):
            data=d.read()
        elif(typename == 'json'):
            import json
            data = json.loads(d.read())
        else:
            print 'read error !please check it !'
    d.close()
    return data
    

#写入序列到文件
def writeFile(string,i,typename): 
    with open(string, 'wb') as d:
        #if(typename == 'seq' or typename == 'key' or typename == 'state' or typename == 'msg'):
        d.write(str(i)) 
    d.close()
    return 1

def resetFile(string):
    f = open(string,'wb')
    f.truncate()
    return

if __name__ == '__main__':
    json = readFile('config.json','json')
    print json
    print json['server_port']
    #print json.dumps(json, indent=4)
