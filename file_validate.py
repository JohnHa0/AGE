import pandas as pd
import os

# 读取Excel文件
file_path = 'D:/HaoProject/AGE/AGE_Classification/data/data_with_labels.xlsx'  # 替换为你的Excel文件路径
# file_path = r'.\data\data_with_labels.xlsx'  # 替换为你的Excel文件路径
df = pd.read_excel(file_path)

# 定义额外的路径信息
additional_path = 'D:/HaoProject/AGE/AGE_Classification/data/'

# 为'File_Path'列的每个文件路径添加额外的路径信息
df['img_idx'] = additional_path + df['img_idx'].astype(str)

# 筛选存在的文件路径
df = df[df['img_idx'].apply(os.path.exists)]

# 文件路径在名为'img_idx'的列中
# df = df[df['img_idx'].apply(lambda x: os.path.exists(str(x)))]

# 保存更改后的Excel文件
df.to_excel('./data/data_with_label_validate.xlsx', index=True)  # 替换为你想要保存的Excel文件路径
