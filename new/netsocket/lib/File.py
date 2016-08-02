#!usr/bin/env python
# -*- coding:utf-8 -*-
__Filename__='File.py'
'''
编写说明：
1. 能正确读写相关文件
2. 最好以二进制格式读写
3. 做好异常处理机制，异常内部raise
4. 现在需要读写的有:json配置文件、包信息本地保存、序列号本地保存、状态机状态本地保存
'''
class File(object):
    '文件读写函数,分别读写json、txt文件(配置文件、包本地保存、状态）'
    def __init__(self,filename,typename='common'):
        self.filename = filename 
        self.typename =  typename

    def ReadFile():
        pass

    def WriteFile():
        pass

