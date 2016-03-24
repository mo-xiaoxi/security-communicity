import struct
datas = ['m1','m2','m3','end']
for i  in range(len(datas)):
    if not datas[i]:
        print "data error"
        break
    tmp=struct.pack("<3si",datas[i],i)
    print tmp
    print len(tmp)
    print struct.unpack("<3si",tmp)

    >>> record = 'raymond   \x32\x12\x08\x01\x08'
>>> name, serialnum, school, gradelevel = unpack('<10sHHb', record)

>>> from collections import namedtuple
>>> Student = namedtuple('Student', 'name serialnum school gradelevel')
>>> Student._make(unpack('<10sHHb', record))
Student(name='raymond   ', serialnum=4658, school=264, gradelevel=8)