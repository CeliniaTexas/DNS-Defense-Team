<<<<<<< HEAD
import subprocess
import time
import os
import sys

PCAP_FILE = "sample.pcap"
CSV_FILE = "dns_traffic.csv"
FEATURE_FILE = "features.txt"
CAPTURE_DURATION = 60  # 抓包时长（秒），可根据需要调整

def capture_traffic(duration=60):
    print(f"开始抓包，持续 {duration} 秒...")
    interface = "5"  # 请根据实际网卡编号调整
    # 只抓取UDP 53端口（DNS）流量
    cmd = [
        "tshark",
        "-i", interface,
        "-a", f"duration:{duration}",
        "-f", "udp port 53",  # 仅抓取DNS流量
        "-w", PCAP_FILE
    ]
    subprocess.run(cmd, check=True)
    print("抓包完成。")

def pcap_to_csv():
    print("正在解析pcap为CSV...")
    tshark_fields = [
        "-T", "fields",
        "-e", "frame.time_epoch",
        "-e", "ip.src",
        "-e", "ip.dst",
        "-e", "dns.qry.name",
        "-e", "dns.qry.type",
        "-e", "dns.resp.type",
        "-e", "dns.txt",
        "-E", "header=y",
        "-E", "separator=,"
    ]
    cmd = ["tshark", "-r", PCAP_FILE] + tshark_fields
    with open(CSV_FILE, "w", encoding="utf-8") as f:
        subprocess.run(cmd, stdout=f, check=True)
    print("CSV解析完成。")

def extract_features():
    print("正在提取特征...")
    script_path = os.path.join(os.path.dirname(__file__), "feature_extractor.py")
    cmd = [sys.executable, script_path]
    with open(FEATURE_FILE, "w", encoding="utf-8") as f:
        subprocess.run(cmd, stdout=f, check=True)
    print(f"特征已保存到 {FEATURE_FILE}")

if __name__ == "__main__":
    capture_traffic(CAPTURE_DURATION)
    pcap_to_csv()
    extract_features()
=======
import subprocess
import time
import os
import sys

PCAP_FILE = "sample.pcap"
CSV_FILE = "dns_traffic.csv"
FEATURE_FILE = "features.txt"
CAPTURE_DURATION = 60  # 抓包时长（秒），可根据需要调整

def capture_traffic(duration=60):
    print(f"开始抓包，持续 {duration} 秒...")
    # 获取网卡编号（假设为1，可用`tshark -D`查看实际编号）
    interface = "5"
    cmd = [
        "tshark",
        "-i", interface,
        "-a", f"duration:{duration}",
        "-w", PCAP_FILE
    ]
    subprocess.run(cmd, check=True)
    print("抓包完成。")

def pcap_to_csv():
    print("正在解析pcap为CSV...")
    tshark_fields = [
        "-T", "fields",
        "-e", "frame.time_epoch",
        "-e", "ip.src",
        "-e", "ip.dst",
        "-e", "dns.qry.name",
        "-e", "dns.qry.type",
        "-e", "dns.resp.type",
        "-e", "dns.txt",
        "-E", "header=y",
        "-E", "separator=,"
    ]
    cmd = ["tshark", "-r", PCAP_FILE] + tshark_fields
    with open(CSV_FILE, "w", encoding="utf-8") as f:
        subprocess.run(cmd, stdout=f, check=True)
    print("CSV解析完成。")

def extract_features():
    print("正在提取特征...")
    script_path = os.path.join(os.path.dirname(__file__), "feature_extractor.py")
    cmd = [sys.executable, script_path]
    with open(FEATURE_FILE, "w", encoding="utf-8") as f:
        subprocess.run(cmd, stdout=f, check=True)
    print(f"特征已保存到 {FEATURE_FILE}")

if __name__ == "__main__":
    capture_traffic(CAPTURE_DURATION)
    pcap_to_csv()
    extract_features()

import subprocess
import time
import os
import sys

PCAP_FILE = "sample.pcap"
CSV_FILE = "dns_traffic.csv"
FEATURE_FILE = "features.txt"
CAPTURE_DURATION = 60  # 抓包时长（秒），可根据需要调整

def capture_traffic(duration=60):
    print(f"开始抓包，持续 {duration} 秒...")
    interface = "5"  # 请根据实际网卡编号调整
    # 只抓取UDP 53端口（DNS）流量
    cmd = [
        "tshark",
        "-i", interface,
        "-a", f"duration:{duration}",
        "-f", "udp port 53",  # 仅抓取DNS流量
        "-w", PCAP_FILE
    ]
    subprocess.run(cmd, check=True)
    print("抓包完成。")

def pcap_to_csv():
    print("正在解析pcap为CSV...")
    tshark_fields = [
        "-T", "fields",
        "-e", "frame.time_epoch",
        "-e", "ip.src",
        "-e", "ip.dst",
        "-e", "dns.qry.name",
        "-e", "dns.qry.type",
        "-e", "dns.resp.type",
        "-e", "dns.txt",
        "-E", "header=y",
        "-E", "separator=,"
    ]
    cmd = ["tshark", "-r", PCAP_FILE] + tshark_fields
    with open(CSV_FILE, "w", encoding="utf-8") as f:
        subprocess.run(cmd, stdout=f, check=True)
    print("CSV解析完成。")

def extract_features():
    print("正在提取特征...")
    script_path = os.path.join(os.path.dirname(__file__), "feature_extractor.py")
    cmd = [sys.executable, script_path]
    with open(FEATURE_FILE, "w", encoding="utf-8") as f:
        subprocess.run(cmd, stdout=f, check=True)
    print(f"特征已保存到 {FEATURE_FILE}")

if __name__ == "__main__":
    capture_traffic(CAPTURE_DURATION)
    pcap_to_csv()
    extract_features()
>>>>>>> acf774f85e1062905e5f90b9b3cbb1e810f2e208
    print("完成。")