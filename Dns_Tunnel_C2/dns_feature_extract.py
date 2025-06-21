import subprocess
import time
import os
import sys

PCAP_FILE = "sample.pcap"
CSV_FILE = "dns_traffic.csv"
FEATURE_FILE = "features.txt"
CAPTURE_DURATION = 120  # 抓包时长（秒），可根据需要调整

def capture_traffic(duration=60):
    print(f"开始抓包，持续 {duration} 秒...")

    # 同时抓取物理网卡和Loopback网卡
    # 物理网卡编号（如WLAN/以太网），请根据实际情况调整
    physical_interface = "5"      # 例如 WLAN
    loopback_interface = "10"     # Loopback 网卡编号

    # 启动两个抓包进程，分别抓取物理网卡和Loopback网卡
    cmds = [
        [
            "tshark",
            "-i", physical_interface,
            "-a", f"duration:{duration}",
            "-f", "udp port 53",
            "-w", "sample_physical.pcap"
        ],
        [
            "tshark",
            "-i", loopback_interface,
            "-a", f"duration:{duration}",
            "-f", "udp port 53",
            "-w", "sample_loopback.pcap"
        ]
    ]

    procs = []
    for cmd in cmds:
        procs.append(subprocess.Popen(cmd))

    # 等待所有抓包进程结束
    for proc in procs:
        proc.wait()

    # 合并两个pcap文件为一个
    print("正在合并pcap文件...")
    merge_cmd = ["mergecap", "-w", PCAP_FILE, "sample_physical.pcap", "sample_loopback.pcap"]
    subprocess.run(merge_cmd, check=True)

    # 删除临时pcap
    os.remove("sample_physical.pcap")
    os.remove("sample_loopback.pcap")

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
    print("完成。")