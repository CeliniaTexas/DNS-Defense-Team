import pandas as pd

# 读取特征文件
df = pd.read_csv('features_scaled.csv')  # 或 features.txt

# 自动标注规则（根据你的C2域名调整）
def label_rule(domain):
    if 'myqcloud.com' in domain:  # 这里根据你的实验C2域名调整
        return 1
    else:
        return 0

df['label'] = df['domain'].apply(label_rule)

# 保存带标签的新文件
df.to_csv('features_labeled.csv', index=False)
print("已添加label标签，保存为 features_labeled.csv")