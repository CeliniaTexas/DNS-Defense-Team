import pandas as pd
from sklearn.preprocessing import StandardScaler

# 读取特征文件
feature_file = 'features.txt'  # 或 'features.txt'，根据实际路径调整
df = pd.read_csv(feature_file)

# 选择需要标准化的特征列（排除domain等非数值列）
feature_cols = [col for col in df.columns if col != 'domain']

# 标准化
scaler = StandardScaler()
df_scaled = df.copy()
df_scaled[feature_cols] = scaler.fit_transform(df[feature_cols])

# 保存标准化后的特征文件
df_scaled.to_csv('features_scaled.csv', index=False)
print("标准化后的特征已保存为 features_scaled.csv")

