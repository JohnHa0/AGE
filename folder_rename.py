import os

def rename_folders(base_path, keywords):
    """
    重命名指定路径下的文件夹，删除关键词列表中的所有关键词。
    
    参数:
    - base_path: 要遍历的文件夹的路径。
    - keywords: 要从文件夹名称中删除的关键词列表。
    """
    # 遍历base_path下的所有文件夹
    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)
        
        # 检查当前路径是否为文件夹
        if os.path.isdir(folder_path):
            new_folder_name = folder_name
            
            # 遍历关键词列表，从文件夹名称中删除关键词
            for keyword in keywords:
                new_folder_name = new_folder_name.replace(keyword, '')
            
            # 重命名文件夹
            new_folder_path = os.path.join(base_path, new_folder_name)
            os.rename(folder_path, new_folder_path)

# 使用示例
base_path = "/path/to/your/directory"  # 替换为你的文件夹路径
keywords = ["keyword1", "keyword2", "keyword3"]  # 替换为你的关键词列表
rename_folders(base_path, keywords)
