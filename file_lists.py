import os
from openpyxl import Workbook

def list_files_in_directory(dir_path):
    """遍历文件夹并返回所有文件的相对路径和文件名"""
    file_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            relative_path = os.path.join(root, file)
            file_list.append((relative_path, file))
    return file_list

def create_excel(file_list, output_file):
    """根据提供的文件列表创建Excel文件"""
    wb = Workbook()
    ws = wb.active
    ws.title = "文件列表"

    # 添加标题行
    ws.append(["相对路径", "文件名"])

    # 添加文件数据
    for file_data in file_list:
        ws.append(file_data)

    wb.save(output_file)

if __name__ == "__main__":
    # directory_path = input("请输入文件夹路径：")
    directory_path = './images'
    # output_file = input("请输入输出Excel文件的路径（例如：output.xlsx）：")
    output_file = './images/file_lists.xlsx'


    files = list_files_in_directory(directory_path)
    create_excel(files, output_file)
    print(f"Excel文件已保存到 {output_file}")

