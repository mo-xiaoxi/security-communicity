'''
每次传入message信息与key异或处理生成新的密钥_key。
然后返回_key
'''
def keyExpand(key,message):
    #message=message[0:48]
    l=len(key)
    key.decode("hex")
    _key = ''.join(chr((ord(c)^ord(k))) for c,k in izip(key, cycle(message)))
    # print('%s ^ %s = %s' % (message, key, cyphered))
    return _key.encode("hex")[:l]
