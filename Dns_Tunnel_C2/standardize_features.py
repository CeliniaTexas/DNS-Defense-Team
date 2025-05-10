import pandas as pd
from sklearn.preprocessing import StandardScaler

# 读取特征文件（假设feature_extractor.py输出为features.csv）
df = pd.read_csv('features.csv')

# 选择需要标准化的数值型特征列（排除domain等非数值列）
num_cols = df.select_dtypes(include=['float64', 'int64']).columns
scaler = StandardScaler()
df[num_cols] = scaler.fit_transform(df[num_cols])

# 保存标准化后的特征
df.to_csv('features_scaled.csv', index=False)
print("标准化完成，已保存为 features_scaled.csv")