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
    if isinstance(string,str):
        with open(string,'rb') as d:
            if(typename == 'seq'):
                data=d.read()
                data=int(data)
            elif(typename == 'key'):
                data=d.read(64)
            elif(typename ==  'msg'):
                data=d.read()
            else:
                print 'read error !please check it !'
        d.close()
        return data
    else:
        return -1

#写入序列到文件
def writeFile(string,i,typename): 
    if isinstance(string,str) and isinstance(string,str):
        if(typename == 'msg'):
                # try:
                #     import cPickle as pickle
                # except ImportError:
                #     import pickle
                # d= open(string, 'a')
                # datas=pickle.dump(i,d)
                with open(string, 'ab') as d:
                     d.write(str(i))
        else:
            with open(string, 'wb') as d:
                if(typename == 'seq'):
                    d.write(str(i)) 
                elif(typename == 'key'):
                    d.write(str(i))
                else:
                    print "write error!"
        d.close()
        return 1
    else:
        return -1
def resetFile(string):
    f = open(string,'wb')
    f.truncate()
    return

if __name__ == '__main__':
    a = ['123','31131','asdas']

    print readFile('test','msg')