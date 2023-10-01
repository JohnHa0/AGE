import pandas as pd
from sklearn.model_selection import train_test_split

# 读取Excel文件
file_path = './data/data_with_label_validate.xlsx'  # 替换为你的Excel文件路径
df = pd.read_excel(file_path)

# 定义数据分割的比例
train_ratio = 0.7
validation_ratio = 0.15
test_ratio = 0.15

# 使用train_test_split函数将数据分割为训练和临时子集
train_data, temp_data = train_test_split(df, test_size=1 - train_ratio, random_state=42)

# 使用train_test_split函数将临时子集分割为验证和预测子集
validation_data, test_data = train_test_split(temp_data, test_size=test_ratio / (test_ratio + validation_ratio),
                                              random_state=42)

# 输出每个子集的大小
print(f"Training data: {len(train_data)} rows")
print(f"Validation data: {len(validation_data)} rows")
print(f"Test data: {len(test_data)} rows")

# 如果需要，可以将这些子集保存到新的Excel文件中
train_data.to_excel('./data/train_data.xlsx', index=False)
validation_data.to_excel('./data/validation_data.xlsx', index=False)
test_data.to_excel('./data/test_data.xlsx', index=False)

train_data.to_csv('./data/train_data.csv', index=False)
validation_data.to_csv('./data/validation_data.csv', index=False)
test_data.to_csv('./data/ntest_data.csv', index=False)
