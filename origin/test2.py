def md5(str):
    import hashlib
    import types
    if type(str) is types.StringType:
        m = hashlib.md5()   
        m.update(str)
        return m.hexdigest()
    else:
        return ''

t1='md5'
t2=t1
test1=md5(t1)
test2=md5(t2)
if test1==test2:
    print "successful"
else:
    print "error"