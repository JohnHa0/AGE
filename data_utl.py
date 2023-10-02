import pandas as pd

# 定义编码
# Gender
gender_encoding = {
    '男': 0,
    '女': 1
}
# Nationality
nation_encoding = {
    '维吾尔族': 0,
    '藏族': 1,
    '回族': 2,
    '汉族': 3,
    '其他': 4,
}

def replace_characters(df):
  # replace gender
  df['gender'] = df['gender'].replace({"男": "Male", "女": "Female"})
  # replace ethnicity 
  replace_dict = {
    "维吾尔族": "Wei",
    "藏族": "Zang",
    "回族": "Hui",
    "汉族": "Han"
    # ... add more replacements as needed
    }
  df['ethnicity'] = df['A'].replace(replace_dict)
  # 为不在替换列表中的值设置固定值"unknown"
  df.loc[~df['ethnicity'].isin(replace_dict.values()), 'ethnicity'] = "Others"
  return df


# Age Bins and Labels
# LABEL_TO_AGE_RANGES = ['0-18', '19-30', '31-40', '41-50', '51-60', '61-80', '81-100']


pd_new = pd.DataFrame()
cols_order = ['img_idx', 'age_label', 'age_cat', 'gender_label', 'ethnicity_label', 'gender', 'ethnicity', 'age']

# 1. 加载Excel文件
df = pd.read_excel("./data/data_fine.xlsx")

# 2. 使用list收集扩展的行数据
expanded_data = []

# 3. 遍历原始dataframe的每一行
for _, row in df.iterrows():
    # 检查照片编号是否为空或缺失
    if pd.isnull(row["照片编号"]) or row["照片编号"] == "":
        continue  # 跳过该行

    # 拆分照片编号
    numbers = row["照片编号"].split("-")

    # 如果有范围的编号，生成该范围内的所有编号
    if len(numbers) == 2:
        start, end = map(int, numbers)
        for num in range(start, end + 1):
            file_path = f"{row['文件夹名']}/IMG_{num}.jpg"
            expanded_data.append({
                "img_idx": file_path,
                "age": row["年龄"],
                "gender": row["性别"],
                "ethnicity": row["民族"]
            })
    # 如果只有一个编号，直接使用该编号
    else:
        file_path = f"{row['文件夹名']}/IMG_{numbers[0]}.jpg"
        expanded_data.append({
            "img_idx": file_path,
            "age": row["年龄"],
            "gender": row["性别"],
            "ethnicity": row["民族"]
        })

# 4. 将收集的数据转换为dataframe
expanded_df = pd.DataFrame(expanded_data)
df_new = pd.DataFrame(columns=cols_order)

df_new['img_idx'] = expanded_df['img_idx']
df_new['gender'] = expanded_df['gender']
df_new['age'] = expanded_df['age']
df_new['ethnicity'] = expanded_df['ethnicity']

# Labeled for gender and nationality

df_new['gender_label'] = expanded_df['gender'].map(gender_encoding)
df_new['ethnicity_label'] = expanded_df['ethnicity'].map(lambda x: nation_encoding.get(x, 8))

# labeled for ages
# LABEL_TO_AGE_RANGES = ['0-18', '19-30', '31-40', '41-50', '51-60', '61-80', '81-100']
bins = [18, 30, 40, 50, 60, 80, 100]
age_ranges = ['18-30', '31-40', '41-50', '51-60', '61-80', '81-100']  # !!!!age =0 will not gain the data !!!!
# age_labels = ['0', '1', '2', '3', '4', '5','6']
# 使用cut函数进行分段编码 Right false 左闭右开
df_new['age_cat'] = pd.cut(expanded_df['age'], bins=bins, labels=age_ranges, right=False)

# 为年龄段提供数字编码，可以再添加一个编码列
age_labels = {label: idx for idx, label in enumerate(age_ranges)}
df_new['age_label'] = df_new['age_cat'].map(age_labels)

# Reorder
# expanded_df = expanded_df[cols_order]
df_new = replace_characters(df_new)
# Save files
df_new.to_excel("./data/data_with_labels.xlsx", index=False)
