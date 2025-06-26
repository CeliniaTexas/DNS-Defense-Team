import csv
import math
from collections import Counter, defaultdict

# 特征表头，便于后续维护和输出
FEATURE_HEADER = [
    "domain", "domain_len", "is_numeric", "qtype",
    "entropy", "depth", "bias",
    "query_freq_per_sec", "req_resp_ratio", "txt_usage_ratio", "min_query_interval"
]

def calc_entropy(domain):
    """计算域名的香农熵，衡量字符分布的复杂度"""
    if not domain:
        return 0.0
    counter = Counter(domain)
    total = len(domain)
    entropy = -sum((count/total) * math.log2(count/total) for count in counter.values() if count > 0)
    return round(entropy, 4)

def label_depth(domain):
    """计算域名的层级深度（点分割）"""
    if not domain:
        return 0
    return len(domain.strip('.').split('.'))

def char_distribution_bias(domain):
    """计算域名字符分布的偏差，衡量字符分布均匀性"""
    if not domain:
        return 0.0
    counter = Counter(domain)
    total = len(domain)
    expected = total / len(counter) if counter else 0
    bias = sum(abs(count - expected) for count in counter.values()) / total if total else 0
    return round(bias, 4)

def extract_features_from_row(row):
    """从单条DNS记录中提取静态特征"""
    domain = row.get("dns.qry.name", "") or ""
    qtype = row.get("dns.qry.type", "") or ""
    domain_len = len(domain)
    is_numeric = domain.replace('.', '').isdigit()
    entropy = calc_entropy(domain)
    depth = label_depth(domain)
    bias = char_distribution_bias(domain)
    return [
        domain,
        domain_len,
        int(is_numeric),
        qtype,
        entropy,
        depth,
        bias
    ]

def safe_float(val, default=0.0):
    """安全地将字符串转换为float，异常返回默认值"""
    try:
        return float(val)
    except (ValueError, TypeError):
        return default

def process_statistics(rows):
    """
    统计全局特征，包括：
    - 查询频率
    - 请求/响应包比例
    - TXT类型使用率
    - 每个域名的最小查询间隔
    """
    time_buckets = defaultdict(list)
    req_resp_count = defaultdict(lambda: {"req": 0, "resp": 0})
    txt_count = 0
    domain_time_dict = defaultdict(list)

    for row in rows:
        # 统计每秒的查询频次
        ts = row.get("frame.time_epoch", "")
        if ts:
            sec = int(safe_float(ts))
            time_buckets[sec].append(row)
            # 记录每个域名的查询时间
            domain = row.get("dns.qry.name", "")
            if domain:
                domain_time_dict[domain].append(safe_float(ts))
        # 统计请求/响应包数量
        if row.get("dns.qry.name", ""):
            req_resp_count["all"]["req"] += 1
        if row.get("dns.resp.type", ""):
            req_resp_count["all"]["resp"] += 1
        # 统计TXT类型查询数量
        if row.get("dns.qry.type", "") == "16":
            txt_count += 1

    # 计算单位时间查询频次（每秒平均）
    if time_buckets:
        freq_per_sec = round(sum(len(v) for v in time_buckets.values()) / len(time_buckets), 4)
    else:
        freq_per_sec = 0.0

    # 计算请求/响应包比例
    req = req_resp_count["all"]["req"]
    resp = req_resp_count["all"]["resp"]
    req_resp_ratio = round(req / resp, 4) if resp else 0.0

    # TXT类型使用率
    txt_usage_ratio = round(txt_count / req, 4) if req else 0.0

    # 计算每个域名的最小查询间隔
    domain_min_interval = {}
    for domain, times in domain_time_dict.items():
        if len(times) > 1:
            sorted_times = sorted(times)
            intervals = [sorted_times[i+1] - sorted_times[i] for i in range(len(sorted_times)-1)]
            min_interval = min(intervals)
        else:
            min_interval = 0.0
        domain_min_interval[domain] = round(min_interval, 4)

    return freq_per_sec, req_resp_ratio, txt_usage_ratio, domain_min_interval

def main():
    input_file = "../data/dns_traffic.csv"
    rows = []
    # 文件读取及异常处理
    try:
        with open(input_file, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # 过滤掉空行或关键字段为空的行
                if not row.get("dns.qry.name", "").strip():
                    continue
                rows.append(row)
    except FileNotFoundError:
        print(f"文件未找到: {input_file}")
        return
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return

    # 统计全局特征
    freq_per_sec, req_resp_ratio, txt_usage_ratio, domain_min_interval = process_statistics(rows)

    # 输出特征表头
    print(",".join(FEATURE_HEADER))
    for row in rows:
        # 再次过滤异常行
        if not row.get("dns.qry.name", "").strip():
            continue
        features = extract_features_from_row(row)
        features.extend([freq_per_sec, req_resp_ratio, txt_usage_ratio])
        domain = row.get("dns.qry.name", "")
        min_interval = domain_min_interval.get(domain, 0.0)
        features.append(min_interval)
        print(",".join(map(str, features)))

if __name__ == "__main__":
    main()