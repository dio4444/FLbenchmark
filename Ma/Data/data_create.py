import numpy as np
import pandas as pd
import random
from sklearn.datasets import make_classification, make_regression

# 生成均匀分布数据集
data_a = np.random.rand(50000, 50)
a_id = random.sample(list(range(1, 70000)), 50000)
a_label = random.choices([0, 1], k=50000)
data_a[:, 0] = np.array(a_id)
data_a = np.column_stack((data_a, np.array(a_label)))
df = pd.DataFrame(data_a)
df.to_csv('rand_a.csv', index=False)

data_b = np.random.rand(40000, 30)
b_id = random.sample(list(range(5000, 90000)), 40000)
data_b[:, 0] = np.array(b_id)
df = pd.DataFrame(data_b)
df.to_csv('rand_b.csv', index=False)

# 生成多维分类数据集
num_samples = 50000
num_features = 50
num_classes = 2
data, labels = make_classification(n_samples=num_samples, n_features=num_features,
                                   n_classes=num_classes, n_informative=35, n_redundant=5,
                                   n_repeated=5, random_state=42, weights=[0.3, 0.7], flip_y=0.02)
# 参数含义： 生成样本数量、特征维数、分类数、有用特征维数、无用特征维数、冗余特征维数、随机种子、类别分布、随机分配类别样本比例
data_labels = np.column_stack((data, labels.T))  # 将数据和标签合并
df = pd.DataFrame(data_labels)
df.to_csv('', index=False)

# 将数据集分成纵向联邦使用的两个数据集
A = random.sample(list(range(num_features)), num_features)
B = A[::2]
A = A[1::2]
dataset_a = np.column_stack((data[:, A], labels.T))
dataset_b = data[:, B]
df = pd.DataFrame()
df.to_csv('', index=False)

# 将数据集分成横向联邦使用的两个数据集
A = random.sample(list(range(num_samples)), num_samples)
B = A[::2]
A = A[1::2]
dataset_a = data_labels[A]
dataset_b = data_labels[B]
df = pd.DataFrame()
df.to_csv('', index=False)

# 生成回归数据集
num_samples = 50000
num_features = 50
X, Y = make_regression(n_samples=num_samples, n_features=num_features,
                       n_informative=40, random_state=42, n_targets=1, noise=1.5)
# n_samples：样本数、n_features：特征数(自变量个数)、n_informative：参与建模特征数、n_targets：因变量个数
# noise：噪音、bias：偏差(截距)、coef：是否输出coef标识、random_state：随机状态若为固定值则每次产生的数据都一样

