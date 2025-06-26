#!/usr/bin/env python3
# paths.py - 项目路径配置

import os

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 主要目录
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "src")
PICTURE_DIR = os.path.join(PROJECT_ROOT, "picture")

# 数据文件
DNS_TRAFFIC_CSV = os.path.join(DATA_DIR, "dns_traffic.csv")
FEATURES_TXT = os.path.join(PROJECT_ROOT, "features.txt")
FEATURES_SCALED_CSV = os.path.join(DATA_DIR, "features_scaled.csv")
FEATURES_LABELED_CSV = os.path.join(DATA_DIR, "features_labeled.csv")
SUSPICIOUS_DOMAINS_CSV = os.path.join(DATA_DIR, "suspicious_domains.csv")
PCAP_FILE = os.path.join(DATA_DIR, "sample.pcap")
SAMPLE_PHYSICAL_PCAP = os.path.join(DATA_DIR, "sample_physical.pcap")
SAMPLE_LOOPBACK_PCAP = os.path.join(DATA_DIR, "sample_loopback.pcap")

# 模型文件
MODEL_FILE = os.path.join(PROJECT_ROOT, "rf_dns_tunnel_model.pkl")

# 确保目录存在
def ensure_directories():
    """确保所有必要的目录存在"""
    directories = [DATA_DIR, MODELS_DIR, OUTPUT_DIR, PICTURE_DIR]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

if __name__ == "__main__":
    # 测试路径配置
    print("📁 项目路径配置:")
    print(f"项目根目录: {PROJECT_ROOT}")
    print(f"数据目录: {DATA_DIR}")
    print(f"模型目录: {MODELS_DIR}")
    print(f"输出目录: {OUTPUT_DIR}")
    print(f"脚本目录: {SCRIPTS_DIR}")
    print(f"图片目录: {PICTURE_DIR}")
