import pandas as pd
import joblib
import os

# 1. 加载模型和特征数据
model_path = 'rf_dns_tunnel_model.pkl'
feature_file = '../data/features_scaled.csv' 

if not os.path.exists(model_path):
    raise FileNotFoundError(f"未找到模型文件: {model_path}，请先训练模型。")
if not os.path.exists(feature_file):
    raise FileNotFoundError(f"未找到特征文件: {feature_file}，请先完成特征提取、标准化和标注。")

df = pd.read_csv(feature_file)
model = joblib.load(model_path)

# 检查必要字段
if 'domain' not in df.columns:
    raise ValueError("特征文件缺少 'domain' 字段。")

X = df.drop(['label', 'domain'], axis=1, errors='ignore')
domains = df['domain']

# 2. 预测
y_pred = model.predict(X)
if hasattr(model, "predict_proba"):
    y_prob = model.predict_proba(X)[:, 1]
else:
    y_prob = [None] * len(y_pred)

# 3. 输出可疑域名清单
result_df = pd.DataFrame({
    'domain': domains,
    'predict': y_pred,
    'confidence': y_prob
})

# 只输出预测为隧道流量（正样本）的域名
suspicious = result_df[result_df['predict'] == 1]
suspicious = suspicious.sort_values(by='confidence', ascending=False)

# 去重，只保留每个域名的第一条记录
suspicious = suspicious.drop_duplicates(subset=['domain'])

print("=== 可疑域名清单（预测为DNS隧道通信） ===")
if suspicious.empty:
    print("未检测到可疑域名。")
else:
    print(suspicious[['domain', 'confidence']].to_string(index=False))

# 4. 保存结果
suspicious.to_csv('../data/suspicious_domains.csv', index=False)
print("可疑域名清单已保存为 ../data/suspicious_domains.csv")