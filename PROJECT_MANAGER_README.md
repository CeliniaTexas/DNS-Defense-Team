# DNS隧道检测项目管理器使用说明

## 📁 项目结构

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
│   └── Figure_1.png              # 分析图表
├── features.txt                   # 原始特征文件
├── README.md                      # 项目说明文档
├── rf_dns_tunnel_model.pkl        # 训练好的随机森林模型
└── run.py                         # 快速启动脚本
```

## 🚀 快速开始

### 方法1：使用快速启动脚本
```bash
cd "DNS-Defense-Team"
python run.py
```

### 方法2：直接运行项目管理器
```bash
cd "DNS-Defense-Team\src"
python project_manager.py
```

## 🎯 项目管理器功能

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

## 📋 数据处理流程

1. **流量生成** → `traffic_gen.py`
2. **特征提取** → `dns_feature_extract.py`
3. **特征标准化** → `standardize_features.py`
4. **添加标签** → `add_label.py`
5. **模型训练** → `model_train.py`
6. **模型检测** → `model_detect.py`

## 🔧 环境要求

- Python 3.x
- 依赖包见 `src/requirements.txt`
- Windows系统（部分功能）
- Wireshark/tshark（用于数据包捕获）

## 📝 注意事项

- 首次运行建议选择"设置项目环境"来安装依赖
- DNS抓包功能需要管理员权限
- 确保网络接口配置正确
- 建议在虚拟环境中运行
