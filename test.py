#!/usr/bin/python
# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
from Crypto.Hash import SHA256

def sha1(text):
    s = SHA256.new()
    s.update(text)
    return s.hexdigest()

aes = AES.new('JG9A90cqiveJ8K7n', AES.MODE_CFB, 'g4vhFIR1KncRIyvO')

text = 'This is some text that will be encrypted'
encrypted_text = aes.encrypt(text)

aes = AES.new('JG9A90cqiveJ8K7n', AES.MODE_CFB, 'g4vhFIR1KncRIyvO')
decrypted_text = aes.decrypt(encrypted_text)

print 'Original:\t' + sha1(text)
print 'Encrypted:\t' + sha1(encrypted_text)
print 'Decrypted:\t' + sha1(decrypted_text)
