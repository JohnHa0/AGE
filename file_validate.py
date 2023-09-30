import pandas as pd
import os

# 读取Excel文件
file_path = './data/data_with_label.xlsx'  # 替换为你的Excel文件路径
df = pd.read_excel(file_path)

# 文件路径在名为'img_idx'的列中
df = df[df['img_idx'].apply(lambda x: os.path.exists(str(x)))]

# 保存更改后的Excel文件
df.to_excel('./data/data_with_label.xlsx', index=False)  # 替换为你想要保存的Excel文件路径
