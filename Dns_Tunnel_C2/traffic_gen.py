# traffic_gen.py  （流量生成模块）

import subprocess  
import time  
import random  
from client import send_command # 复用client.py中的send_command函数  
import dns.resolver # 用于生成正常DNS流量  

def generate_tunnel_traffic(num_commands=10):  
    """生成模拟的DNS隧道流量（正样本）"""  
    print(f"正在生成 {num_commands} 条模拟隧道命令...") 
    
    commands = [  
        #这些是linux命令，所以在window上输入这些命令会失败 
        # "whoami",  
        # "hostname",  
        # "pwd",  
        # "ls -l",  
        # "cat /etc/passwd", # 示例敏感命令  
        # "date",  
        # "uname -a",  
        # "ip addr show",  
        # "ps aux",  
        # "df -h"  
        #-------------------------
        #这些是windows命令
        "whoami",
        "hostname",
        "dir",                # 列出当前目录文件
        "type C:\\Windows\\win.ini",  # 查看文件内容
        "echo hello world",   # 输出文本
        "date /T",            # 显示当前日期
        "time /T",            # 显示当前时间
        "ipconfig",           # 查看IP配置
        "tasklist",           # 查看进程列表
        #   "systeminfo"          # 查看系统信息，内容过多，会超时
    ]  

    for _ in range(num_commands):  
        command = random.choice(commands)  
        print(f"发送模拟命令: {command}")  
        send_command(command)  
        time.sleep(random.uniform(2, 5)) # 随机等待2~5秒，模拟真实流量间隔

def generate_normal_dns_traffic(num_queries=20):  
    """生成模拟的正常DNS流量（负样本）"""  
    print(f"正在生成 {num_queries} 条模拟正常DNS查询...")  
    domains = [  
        "google.com",  
        "github.com",  
        "twitter.com",  
        "facebook.com",  
        "amazon.com",  
        "wikipedia.org",  
        "reddit.com",  
        "linkedin.com",  
        "microsoft.com",  
        "apple.com"  
    ]  

    for _ in range(num_queries):  
        domain = random.choice(domains)  
        try:  
            # 为正常流量模拟使用不同的解析器，  
            # 或配置系统默认的DNS解析器。  
            # 这里示例使用公共DNS服务器进行正常流量查询。  
            resolver = dns.resolver.Resolver()  
            resolver.nameservers = ['8.8.8.8'] # Google 公共DNS  
            answers = resolver.resolve(domain, 'A')  
            print(f"成功查询 {domain}。")  
        except Exception as e:  
            print(f"查询 {domain} 失败: {e}")  
        time.sleep(random.uniform(0.5, 2)) # 随机等待0.5~2秒，模拟真实间隔

if __name__ == "__main__":  
    print("正在生成训练数据...")  

    # 生成正样本（隧道流量）  
    print("\n--- 生成正样本（隧道流量） ---")  
    generate_tunnel_traffic(num_commands=20)  

    # 生成负样本（正常DNS流量）  
    print("\n--- 生成负样本（正常DNS流量） ---")  
    generate_normal_dns_traffic(num_queries=50)  

    print("\n训练数据生成完毕。")