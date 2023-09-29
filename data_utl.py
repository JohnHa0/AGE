import pandas as pd

# 定义编码
gender_encoding = {
    '男': 0,
    '女': 1
}

nation_encoding = {
    '藏族': 0,
    '回族': 1,
    '汉族': 2,
    '维吾尔族': 3,
    '满族': 4,
    '蒙古族': 5,
    '彝族': 6,
    '朝鲜族': 7,
    '其他': 8,
}



# 读取Excel文件
df = pd.read_excel("./data/data_fine.xlsx")
# Labeled
df['性别'] = df['性别'].map(gender_encoding)
df['民族'] = df['民族'].map(lambda x: nation_encoding.get(x, 8))

# Generate file path
def generate_file_names(folder, number_pattern):
    if '-' in number_pattern:
        start, end = map(int, number_pattern.split('-'))
        return [f"{folder}/{i}.jpg" for i in range(start, end + 1)]
    else:
        return [f"{folder}/{number_pattern}.jpg"]

all_paths = []
folder_names = df.iloc[:, 0].values
jpg_numbers = df.iloc[:, -1].values
for folder, number_pattern in zip(folder_names, jpg_numbers):
    all_paths.extend(generate_file_names(folder, number_pattern))

df_full_paths = pd.DataFrame({"完整路径": all_paths})
# Save files
df_full_paths.to_excel("./data/data_label.xlsx", index=False)


