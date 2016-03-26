from cryption import aes,hmac,getNeededKey,messageExchangge,keyExpand,packetFill


#test aes
key = '1234567891234567'  # Store this somewhere safe
aestest = aes.prpcrypt(key)
ciphertext = aestest.encrypt('M1')
print ciphertext
plaintext = aestest.decrypt(ciphertext)
print plaintext

#test hmac
h = hmac.hmac_md5("key", "Im ted")
print h.hexdigest()

#test getNeededKey
key = '123456789qwertyuio'
for i in range(3):
    an = getNeededKey.getkey(key,i)
    print an


#test  messageExchangge
print messageExchangge.m_exchange("abcdefsdfswerd")
#test  keyExpand
k="284268746382"
m="msdfd1"
print keyExpand.xor_string(k, m)
#test  packetFill
message='1231'
x=987987
m,y=packetFill.packetFill(message,x)
print m,y
print packetFill.re_packetFill(m,y)
