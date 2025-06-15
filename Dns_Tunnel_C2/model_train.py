import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import joblib
import os

# 1. 读取特征数据
feature_file = 'features_labeled.csv'  # 使用最新带label的csv
if not os.path.exists(feature_file):
    raise FileNotFoundError(f"未找到特征文件: {feature_file}，请先完成特征提取、标准化和标注。")

df = pd.read_csv(feature_file)

# 检查必要字段
required_cols = {'label', 'domain'}
if not required_cols.issubset(df.columns):
    raise ValueError(f"特征文件缺少必要字段: {required_cols}，请补充标签。")

X = df.drop(['label', 'domain'], axis=1)
y = df['label']

# 2. 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# 3. 随机森林模型训练与参数优化
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [5, 10, None]
}
clf = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=3,
    scoring='f1',
    n_jobs=-1
)
clf.fit(X_train, y_train)
best_model = clf.best_estimator_

# 4. 模型评估
y_pred = best_model.predict(X_test)
y_prob = best_model.predict_proba(X_test)[:, 1]

print("=== 分类报告 ===")
print(classification_report(y_test, y_pred, digits=4))
print("=== 混淆矩阵 ===")
print(confusion_matrix(y_test, y_pred))
print("=== AUC分数 ===")
print(roc_auc_score(y_test, y_prob))

# 5. 可视化ROC曲线
fpr, tpr, _ = roc_curve(y_test, y_prob)
plt.figure()
plt.plot(fpr, tpr, label='ROC curve (AUC = %.4f)' % roc_auc_score(y_test, y_prob))
plt.plot([0, 1], [0, 1], 'k--', label='Random')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.tight_layout()
plt.show()

# 6. 输出特征重要性
importances = best_model.feature_importances_
feature_names = X.columns
importance_df = pd.DataFrame({'feature': feature_names, 'importance': importances})
importance_df = importance_df.sort_values(by='importance', ascending=False)
print("=== 特征重要性排序 ===")
print(importance_df)

# 7. 保存模型
joblib.dump(best_model, 'rf_dns_tunnel_model.pkl')
print("模型已保存为 rf_dns_tunnel_model.pkl")