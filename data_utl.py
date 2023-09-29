import pandas as pd

# 定义编码
# Gender
gender_encoding = {
    '男': 0,
    '女': 1
}
# Nationality
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

# Age Bins and Labels
# LABEL_TO_AGE_RANGES = ['0-18', '19-30', '31-40', '41-50', '51-60', '61-80', '81-100']



pd_new = pd.DataFrame()
cols_order = ['img_idx', 'age_label','age_cat','gender_label','ethnicity_label','gender','ethnicity','age']



# 读取Excel文件
df = pd.read_excel("./data/data_fine.xlsx")

# Generate file path
def generate_file_names(folder, number_pattern):
    if isinstance(number_pattern, str):
        if '-' in number_pattern:
            start, end = map(int, number_pattern.split('-'))
            return [f"{folder}/{i}.jpg" for i in range(start, end + 1)]
        else:
            return [f"{folder}/{number_pattern}.jpg"]
    return []

all_paths = []
folder_names = df.iloc[:, 0].values
jpg_numbers = df.iloc[:, -1].values
for folder, number_pattern in zip(folder_names, jpg_numbers):
    all_paths.extend(generate_file_names(folder, number_pattern))

# df_full_paths = pd.DataFrame({"完整路径": all_paths})
pd_new['img_idx'] = all_paths

# Labeled for gender and nationality
pd_new['gender'] = df['性别']
pd_new['ethnicity'] = df['民族']
pd_new['age'] = df['年龄']
pd_new['gender_label'] = df['性别'].map(gender_encoding)
pd_new['ethnicity_label'] = df['民族'].map(lambda x: nation_encoding.get(x, 8))

# labeled for ages
# LABEL_TO_AGE_RANGES = ['0-18', '19-30', '31-40', '41-50', '51-60', '61-80', '81-100']
bins = [18, 30, 40, 50, 60, 80, 100]
age_ranges= ['18-30', '31-40', '41-50', '51-60', '61-80', '81-100']
# age_labels = ['0', '1', '2', '3', '4', '5','6']
# 使用cut函数进行分段编码 Right false 左闭右开
pd_new['age_cat'] = pd.cut(df['年龄'], bins=bins, labels=age_ranges, right=False)

# 为年龄段提供数字编码，可以再添加一个编码列
age_labels = {label: idx for idx, label in enumerate(age_ranges)}
pd_new['age_label'] = pd_new['age_cat'].map(age_labels)



# Reorder
pd_new = pd_new[cols_order]
# Save files
pd_new.to_excel("./data/data_with_labels.xlsx", index=False)


