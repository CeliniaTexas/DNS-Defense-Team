import subprocess
import time
import os
import sys

PCAP_FILE = "sample.pcap"           # 合并后的pcap文件名
CSV_FILE = "../data/dns_traffic.csv"        # 解析后的CSV文件名
FEATURE_FILE = "features.txt"       # 提取特征保存的文件名
CAPTURE_DURATION = 3600             # 抓包时长（秒），可根据需要调整

def capture_traffic(duration=60):
    print(f"开始抓包，持续 {duration} 秒...")

    # 指定物理网卡和Loopback网卡编号（需根据实际环境调整）
    physical_interface = "5"      # 物理网卡编号
    loopback_interface = "10"     # Loopback网卡编号

    # 启动两个抓包进程，分别抓取物理网卡和Loopback网卡的DNS流量
    cmds = [
        [
            "tshark",
            "-i", physical_interface,
            "-a", f"duration:{duration}",
            "-f", "udp port 53",
            "-w", "../data/sample_physical.pcap"
        ],
        [
            "tshark",
            "-i", loopback_interface,
            "-a", f"duration:{duration}",
            "-f", "udp port 53",
            "-w", "../data/sample_loopback.pcap"
        ]
    ]

    procs = []
    for cmd in cmds:
        procs.append(subprocess.Popen(cmd))  # 启动抓包进程

    # 等待所有抓包进程结束
    for proc in procs:
        proc.wait()    # 合并两个pcap文件为一个
    print("正在合并pcap文件...")
    merge_cmd = ["mergecap", "-w", PCAP_FILE, "../data/sample_physical.pcap", "../data/sample_loopback.pcap"]
    subprocess.run(merge_cmd, check=True)

    # 删除临时pcap文件
    os.remove("../data/sample_physical.pcap")
    os.remove("../data/sample_loopback.pcap")

    print("抓包完成。")

def pcap_to_csv():
    print("正在解析pcap为CSV...")
    # 指定tshark导出字段
    tshark_fields = [
        "-T", "fields",
        "-e", "frame.time_epoch",   # 时间戳
        "-e", "ip.src",             # 源IP
        "-e", "ip.dst",             # 目的IP
        "-e", "dns.qry.name",       # 查询域名
        "-e", "dns.qry.type",       # 查询类型
        "-e", "dns.resp.type",      # 响应类型
        "-e", "dns.txt",            # TXT记录内容
        "-E", "header=y",           # 输出表头
        "-E", "separator=,"         # 逗号分隔
    ]
    cmd = ["tshark", "-r", PCAP_FILE] + tshark_fields
    with open(CSV_FILE, "w", encoding="utf-8") as f:
        subprocess.run(cmd, stdout=f, check=True)
    print("CSV解析完成。")

def extract_features():
    print("正在提取特征...")
    # 调用特征提取脚本，将结果输出到FEATURE_FILE
    script_path = os.path.join(os.path.dirname(__file__), "feature_extractor.py")
    cmd = [sys.executable, script_path]
    with open(FEATURE_FILE, "w", encoding="utf-8") as f:
        subprocess.run(cmd, stdout=f, check=True)
    print(f"特征已保存到 {FEATURE_FILE}")

if __name__ == "__main__":
    capture_traffic(CAPTURE_DURATION)  # 抓取DNS流量
    pcap_to_csv()                      # 解析pcap为CSV
    extract_features()                 # 提取特征
    print("完成。")