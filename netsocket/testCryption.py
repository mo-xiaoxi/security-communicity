from cryption import aes,hmac,getNeededKey
key = 'Some arbitrary bytestring.'  # Store this somewhere safe
aestest = aes.AES(key)
ciphertext = aestest.encrypt('M1')
print ciphertext
plaintext = aestest.decrypt(ciphertext)
print plaintext

h = hmac.hmac_md5("key", "Im ted")
print h.hexdigest()

key = '123456789qwertyuio'
for i in range(3):
    an = getNeededKey.getNeededkey1(key,i)
    print an