# 使用说明
# DNS-Defense-Team-main / Dns_Tunnel_C2

## 项目简介

本项目实现了一个基于 DNS 隧道的 C2 通信模拟与检测系统，涵盖流量生成、特征提取、特征标准化、自动标注、模型训练与检测等完整流程。适用于安全研究、流量分析、机器学习建模等场景。

---

## 项目原理

- **DNS隧道通信**：把命令内容（如 `echo hello`）Base64编码后作为子域名（如 `ZWNobyBoZWxsbw==.localtest.com`），通过DNS查询伪装传输，实现隐蔽的数据通信。
- **服务端解析**：服务端收到DNS请求，提取子域名并解码执行命令，将结果加密后通过DNS TXT记录返回。
- **客户端解密**：客户端收到响应后解密，还原命令输出。

---

##  项目结构

```
DNS-Defense-Team/
├── data/                          # 数据文件目录
│   ├── dns_traffic.csv            # DNS流量数据
│   ├── features_labeled.csv       # 带标签的特征数据
│   ├── features_scaled.csv        # 标准化后的特征数据
│   ├── suspicious_domains.csv     # 可疑域名清单
│   ├── sample_loopback.pcap       # 回环网卡抓包文件
│   └── sample_physical.pcap       # 物理网卡抓包文件
├── src/                           # Python源代码目录
│   ├── add_label.py               # 添加标签脚本
│   ├── client.py                  # DNS隧道客户端
│   ├── config.py                  # 配置文件
│   ├── crypto.py                  # 加密模块
│   ├── dns_feature_extract.py     # DNS特征提取
│   ├── feature_extractor.py       # 特征提取器
│   ├── model_detect.py            # 模型检测
│   ├── model_train.py             # 模型训练
│   ├── paths.py                   # 路径配置
│   ├── project_manager.py         # 项目管理器
│   ├── server.py                  # DNS隧道服务器
│   ├── standardize_features.py    # 特征标准化
│   ├── traffic_gen.py             # 流量生成
│   └── requirements.txt           # 依赖包清单
├── models/                        # 模型文件目录
├── output/                        # 输出文件目录
├── picture/                       # 图片文件目录
├── features.txt                   # 原始特征文件
├── README.md                      # 项目说明文档
├── rf_dns_tunnel_model.pkl        # 训练好的随机森林模型
└── run.py                         # 快速启动脚本
```
---

## 使用方法

### 1. 配置环境

- 安装依赖：`pip install -r requirements.txt`
- 配置 `config.py`，设置你的 ROOT_DOMAIN（如 `localtest.com`）和 AES_KEY。

### 2. 启动 DNS 隧道服务端

```bash
python server.py
```
> 需管理员权限监听 53 端口。

### 3. 生成训练流量

```bash
python traffic_gen.py
```
- 自动生成正样本（隧道流量，label=1）和负样本（正常DNS流量，label=0）。

### 4. 抓包与特征提取

```bash
python dns_feature_extract.py
```
- 自动抓取 DNS 流量，生成 `dns_traffic.csv`。
- 自动调用 `feature_extractor.py` 提取特征，生成 `features.txt`。

### 5. 特征标准化

```bash
python standardize_features.py
```
- 输入：`features.txt`
- 输出：`features_scaled.csv`

### 6. 自动标注正负样本

```bash
python add_label.py
```
- 输入：`features_scaled.csv`
- 输出：`features_labeled.csv`
- 标注规则：如 `myqcloud.com` 为正样本，其它为负样本（可在 `add_label.py` 中自定义）。

### 7. 检测模型训练与评估

```bash
python model_train.py
```
- 输入：`features_labeled.csv`
- 输出：`rf_dns_tunnel_model.pkl`
- 自动输出分类报告、混淆矩阵、AUC、特征重要性等。

### 8. 检测与告警

```bash
python model_detect.py
```
- 输入：`features_labeled.csv` 或新特征文件
- 输出：`suspicious_domains.csv`（可疑域名清单）

---

## 正负样本区分说明

- **正样本（label=1）**：由 `traffic_gen.py` 的 `generate_tunnel_traffic` 产生，域名包含你的 C2 根域名（如 `myqcloud.com`、`localtest.com`）。
- **负样本（label=0）**：由 `generate_normal_dns_traffic` 产生，域名为常见互联网域名（如 `google.com`、`baidu.com`）。

自动标注规则可在 `add_label.py` 中自定义。

---

## 本地模拟方法

在没有真实域名和独立DNS服务器的情况下，可以本地模拟：

1. 修改 `config.py`，将 ROOT_DOMAIN 设置为如 "localtest.com"。
2. 修改本地 hosts 文件，将该域名指向 127.0.0.1。
   ```
   127.0.0.1    localtest.com
   ```
3. 启动 server.py 和 client.py，所有DNS请求均在本地完成，便于测试和流量生成。

---

## 常见问题

- **端口占用/权限问题**：监听 53 端口需管理员权限。
- **特征文件缺失/格式错误**：请严格按照流程依次生成和处理文件。
- **标注规则不符**：请根据实际 C2 域名修改 `add_label.py` 的判断逻辑。

---

## 免责声明

本项目仅供网络安全研究与教学使用，严禁用于任何非法用途。

---

## 参考命令

```bash
# 典型全流程
python server.py
python traffic_gen.py
python dns_feature_extract.py
python standardize_features.py
python add_label.py
python model_train.py
python model_detect.py
```

---


##  快速开始

### 方法：直接运行项目管理器
```bash
cd "DNS-Defense-Team\src"
python project_manager.py
```

##  项目管理器功能

1. **查看项目结构** - 显示所有文件的状态和大小
2. **运行完整数据管道** - 自动执行完整的数据处理流程
3. **生成训练数据** - 运行流量生成脚本
4. **提取DNS特征** - 从PCAP文件提取特征
5. **标准化特征** - 对特征进行标准化处理
6. **添加标签** - 为数据添加分类标签
7. **训练模型** - 训练机器学习模型
8. **运行检测** - 使用训练好的模型进行检测
9. **启动DNS隧道服务器** - 启动DNS隧道服务端
10. **启动DNS隧道客户端** - 启动DNS隧道客户端
11. **清理数据文件** - 清理所有生成的数据文件
12. **设置项目环境** - 安装依赖并创建必要目录



##  环境要求

- Python 3.x
- 依赖包见 `src/requirements.txt`
- Windows系统（部分功能）
- Wireshark/tshark（用于数据包捕获）

##  注意事项

- 首次运行建议选择"设置项目环境"来安装依赖
- DNS抓包功能需要管理员权限
- 确保网络接口配置正确
- 建议在虚拟环境中运行
