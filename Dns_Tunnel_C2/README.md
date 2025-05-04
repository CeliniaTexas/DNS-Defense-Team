README.md
简介
把命令变成子域名，就是把数据“伪装”成正常的DNS查询，实现数据的隐蔽传输。
1. DNS协议允许查询任意域名
- DNS查询时，客户端可以请求任何合法的域名，比如 abc.localtest.com。
- 域名的子域部分（如 abc）可以被自由拼接和编码。

---
2. 利用子域名传递数据
- 把命令内容（如 echo hello）经过Base64编码，变成只包含字母和数字的字符串（如 ZWNobyBoZWxsbw==）。
- 再把这个字符串作为子域名的一部分，比如 ZWNobyBoZWxsbw==.localtest.com。
- 这样，命令内容就“藏”在了DNS查询的域名里。

代码结构：
dns_tunnel_c2/  
├── server.py              # DNS 服务器 (C2)  
├── client.py              # 客户端 (被控端)  
├── crypto.py              # 加密模块  
├── traffic_gen.py         # 流量生成模块  
├── config.py              # 配置文件 (例如：根域名, AES 密钥)  
├── dns_feature_extract.py # DNS流量抓包与特征提取自动化脚本  
├── feature_extractor.py   # DNS流量特征提取脚本  
└── README.md              # 说明文件  

使用方法：
配置：
在 config.py 中设置你的 ROOT_DOMAIN. 你需要拥有这个域名的控制权，并在你的 DNS 服务器上设置相应的 NS 或 A 记录指向运行 server.py 的机器。
设置一个安全的 AES_KEY.

运行 C2 服务器：
python server.py  
确保你的防火墙允许 UDP 端口 53 的流量进入。

运行客户端 (被控端)：
python client.py  
客户端会连接到本地的 53 端口，发送命令并接收结果。
在运行 client.py 后，直接在提示符下输入你想让服务端执行的系统命令。例如：

whoami （查看当前用户名）
ipconfig （Windows下查看IP信息）
echo hello （输出 hello）
dir （Windows下列出当前目录文件）
quit （退出客户端）

生成训练流量：
python traffic_gen.py  
运行这个脚本会生成模拟的 DNS 隧道流量和正常的 DNS 流量。你可以使用 Wireshark 等工具捕获这些流量，并将其用于模型训练。

注意事项：

权限： 在某些操作系统上，运行在端口 53 的服务需要 root/管理员权限。
域名设置： ROOT_DOMAIN 的设置至关重要。你需要配置你的 DNS 记录，使得 *.your_root_domain.com 的 DNS 请求被导向运行 server.py 的机器。
实际应用： 这个工具是用于模拟和教育目的的。在实际的渗透测试或红队行动中，需要更强大的功能和更复杂的隐蔽技术。
流量捕获： 使用 tcpdump 或 Wireshark 捕获发送到端口 53 的 UDP 流量，以便分析和用于模型训练。

注：本地模拟方法
在没有域名和独立DNS服务器的情况下，进行本地模拟的步骤：
修改 config.py： 将 ROOT_DOMAIN 设置为希望模拟的域名，例如 "localtest.com"。
修改本地hosts文件： 将 config.py 中设置的模拟域名指向本地IP地址（通常是 127.0.0.1）。
127.0.0.1    localtest.com  

运行 server.py： 在本地计算机上启动模拟的C2服务器。
python server.py  
运行 client.py 或 traffic_gen.py： 在本地计算机上运行客户端或流量生成脚本。它们会将DNS请求发送到本地的模拟DNS服务器。
这样，你就可以在本地环境中模拟DNS隧道通信和生成相应的流量了。虽然没有真实的外部域名和DNS服务器，但这个设置足以让你理解和测试DNS隧道的工作原理，并生成用于模型训练的本地流量。


启动server.py和client.py后，在client.py中输入命令
echo hello
1. 客户端编码命令并发送DNS请求
你输入 echo hello，客户端将其用 Base64 编码为 ZWNobyBoZWxsbw==。
客户端将编码后的命令拼接成子域名，形成完整的查询域名（如 ZWNobyBoZWxsbw==.localtest.com）。
客户端通过 DNS 查询（类型为 TXT）把这个域名请求发送到本地的 C2 服务器（你的 server.py）。

2. 服务端接收并处理请求
服务端收到 DNS 查询，提取出子域名部分，Base64 解码还原出原始命令 echo hello。
服务端在操作系统上执行该命令，得到输出 hello。
服务端用 AES 密钥对输出结果加密，再用 Base64 编码，放入 DNS TXT 记录作为响应返回给客户端。

3. 客户端接收并解密响应
客户端收到 DNS TXT 记录，将内容 Base64 解码，再用 AES 密钥解密，还原出命令的输出结果。
客户端在终端打印出：
--- 命令输出 ---
hello

运行dns_feature_extract.py：对server.py和client.py产生的流量使用T-shark抓取指定时长的网络流量，保存为`sample.pcap`
然后调用feature_extractor.py将pcap文件解析为csv格式，提取关心的字段（如时间戳、源/目的IP、查询域名、类型等）
特征集经标准化后存入txt文件
----------------
