# crypto.py  

from Crypto.Cipher import AES  
from Crypto.Util.Padding import pad, unpad  
from Crypto.Random import get_random_bytes  
from config import AES_KEY  

class AESCipher:  
    def __init__(self, key):  
        self.key = key  

    def encrypt(self, data):  
        cipher = AES.new(self.key, AES.MODE_CBC)  
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))  
        return cipher.iv + ct_bytes  

    def decrypt(self, data):  
        iv = data[:AES.block_size]  
        ct = data[AES.block_size:]  
        cipher = AES.new(self.key, AES.MODE_CBC, iv)  
        pt = unpad(cipher.decrypt(ct), AES.block_size)  
        return pt  