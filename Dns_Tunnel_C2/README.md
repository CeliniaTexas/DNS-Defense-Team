# 一、简介

本作品提出一种结合流量特征分析与轻量级机器学习的检测方案，旨在解决传统规则匹配方法误报率高、难以应对动态变种的问题。

# 二. 相关工作

## 1.制作DNS隧道模拟工具

基于Python的dnslib库开发C2模拟工具，支持两种隐蔽通信模式：

子域名指令传递：将Base64编码的命令拆分为多级子域名（如ZmxhZw.gw1.example.com代表"flag"指令）；

TXT记录回传：通过DNS响应包中的TXT字段返回执行结果，数据经AES加密后分段传输。
该工具可生成用于模型训练的正、负样本流量。

## 2.制作多维特征提取引擎

利用TSHark对原始流量进行预处理，提取三类特征：

①统计特征：单位时间内的查询频次、请求/响应包比例；

②结构特征：域名熵值（衡量随机性）、标签层级深度、字符分布偏离度；

③行为特征：非常规记录类型（如TXT）使用率、周期性查询模式。
特征集经标准化后存入时序数据库，供模型动态更新。

## 3.制作轻量级检测模型

采用Scikit-learn构建随机森林分类器，通过Pipeline集成特征选择（方差过滤）与参数优化（网格搜索）。模型以F1-score为核心指标，支持在线增量学习以适应新型攻击变种。检测结果生成带置信度的可疑域名清单，并联动威胁情报平台进行二次验证。



# 三、项目结构：

 ```bash
dns_tunnel_c2/

├── server.py # DNS 服务器 (C2)
├── client.py # 客户端 (被控端)
├── crypto.py # 加密模块
├── traffic_gen.py # 流量生成模块
├── config.py # 配置文件 (例如：根域名, AES 密钥)
├── dns_feature_extract.py # DNS流量抓包与特征提取自动化脚本
├── feature_extractor.py # DNS流量特征提取脚本
└── README.md # 说明文件
 ```

 

# 四、使用方法：

1. 配置： 在 config.py 中设置 ROOT_DOMAIN. 我们需要拥有这个域名的控制权，并在 DNS 服务器上设置相应的 NS 或 A 记录指向运行 server.py 的机器。 设置一个安全的 AES_KEY.

2. 运行 C2 服务器： 

   ```bash
   python server.py
   ```


   确保防火墙允许 UDP 端口 53 的流量进入。

3. 运行客户端 (被控端)：

   ```bash
    python client.py
   ```

   客户端会连接到本地的 53 端口，发送命令并接收结果。 在运行 client.py 后，直接在提示符下输入想让服务端执行的系统命令。例如：

   ```bash
   whoami 		//查看当前用户名
   ipconfig 	//Windows下查看IP信息
   echo hello 	//输出 hello
   dir 		//Windows下列出当前目录文件
   quit 		//退出客户端
   ```

4. 生成训练流量：

   ```bash
    python traffic_gen.py
   ```

   ​	运行这个脚本会生成模拟的 DNS 隧道流量和正常的 DNS 流量。你可以使用 Wireshark 等工具捕获这些流量，并将其用于模型训练。

   

5. 运行dns_feature_extract.py：

   ```bash
    python dns_feature_extract.py
   ```

   ​	对server.py和client.py产生的流量使用T-shark抓取指定时长的网络流量，保存为`sample.pcap`从 DNS 相关的数据（如域名、查询类型、响应码等）中提取有用的特征，例如域名长度、是否包含数字、是否有特殊字符、查询频率

   dns_feature_extract.py会自动调用feature_extractor.py将pcap文件解析为csv格式，提取关心的字段（如时间戳、源/目的IP、查询域名、类型等）特征集经标准化后存入txt文件.

   

## 注意事项：

1.权限： 在某些操作系统上，运行在端口 53 的服务需要 root/管理员权限。

2.域名设置： ROOT_DOMAIN 的设置至关重要。需要配置机器的DNS 记录，使得 *.your_root_domain.com 的 DNS 请求被导向运行 server.py 的机器。 

3.实际应用： 这个工具是用于模拟和教育目的的。在实际的渗透测试或红队行动中，需要更强大的功能和更复杂的隐蔽技术。 

4.流量捕获： 使用 tcpdump 或 Wireshark 捕获发送到端口 53 的 UDP 流量，以便分析和用于模型训练。

 

## 注：本地模拟方法

在没有域名和独立DNS服务器的情况下，进行本地模拟的步骤： 

1. 修改 config.py： 将 ROOT_DOMAIN 设置我们为希望模拟的域名，例如 "localtest.com"

2. 修改本地hosts文件： 将 config.py 中设置的模拟域名指向本地IP地址（通常是 127.0.0.1）

3.  运行 server.py： 在本地计算机上启动模拟的C2服务器。

   ```bash
    python server.py
   ```

4. 运行 client.py 或 traffic_gen.py： 在本地计算机上运行客户端或流量生成脚本。它们会将DNS请求发送到本地的模拟DNS服务器。这样就可以在本地环境中模拟DNS隧道通信和生成相应的流量了。虽然没有真实的外部域名和DNS服务器，但这个设置足以测试DNS隧道的工作原理，并生成用于模型训练的本地流量。

   启动server.py和client.py后，在client.py中输入命令 

   ```bash
   echo hello
   ```

   

5. 客户端编码命令并发送DNS请求。输入 echo hello，客户端将其用 Base64 编码为 ZWNobyBoZWxsbw==。 客户端将编码后的命令拼接成子域名，形成完整的查询域名（如 ZWNobyBoZWxsbw==.localtest.com）。 客户端通过 DNS 查询（类型为 TXT）把这个域名请求发送到本地的 C2 服务器（server.py）。

6. 服务端接收并处理请求 服务端收到 DNS 查询，提取出子域名部分，Base64 解码还原出原始命令 echo hello。 服务端在操作系统上执行该命令，得到输出 hello。 服务端用 AES 密钥对输出结果加密，再用 Base64 编码，放入 DNS TXT 记录作为响应返回给客户端。

7. 客户端接收并解密响应 客户端收到 DNS TXT 记录，将内容 Base64 解码，再用 AES 密钥解密，还原出命令的输出结果。 客户端在终端打印出： --- 命令输出 --- hello.