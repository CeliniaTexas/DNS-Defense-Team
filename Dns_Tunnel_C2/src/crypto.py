# crypto.py  

from Crypto.Cipher import AES  # 导入AES加密算法
from Crypto.Util.Padding import pad, unpad  # 导入填充和去填充方法
from Crypto.Random import get_random_bytes  # 导入生成随机字节的方法
from config import AES_KEY  # 导入配置文件中的AES密钥

class AESCipher:  
    def __init__(self, key):  
        self.key = key  # 初始化时设置密钥

    def encrypt(self, data):  
        # 创建一个新的AES加密器，使用CBC模式，每次加密生成新的随机IV
        cipher = AES.new(self.key, AES.MODE_CBC)  
        # 对数据进行填充并加密
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))  
        # 返回IV和密文拼接后的结果
        return cipher.iv + ct_bytes  

    def decrypt(self, data):  
        # 提取前16字节作为IV
        iv = data[:AES.block_size]  
        # 剩余部分为密文
        ct = data[AES.block_size:]  
        # 创建AES解密器，使用相同的密钥和IV
        cipher = AES.new(self.key, AES.MODE_CBC, iv)  
        # 解密并去除填充，得到明文
        pt = unpad(cipher.decrypt(ct), AES.block_size)  
        return pt