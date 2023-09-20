#
# FrontFace Photo Extractions.
# REQUIREMENTS: pip install face_recognition before usage
# SET the image source folder and then type the destination path for the extracted photos.
# JohnHA0
# 2023.09.15
# import face_recognition
# import os
# import shutil
#
# def is_frontal_face(image_path):
#     image = face_recognition.load_image_file(image_path)
#
#     # 使用face_recognition库进行人脸检测
#     face_locations = face_recognition.face_locations(image)
#
#     # 如果有一个以上的脸或没有脸，我们认为它不是正面照片
#     if len(face_locations) != 1:
#         return False
#     return True
#
# def filter_frontal_faces(source_dir, target_dir):
#     if not os.path.exists(target_dir):
#         os.makedirs(target_dir)
#
#     for filename in os.listdir(source_dir):
#         if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
#             filepath = os.path.join(source_dir, filename)
#
#             if is_frontal_face(filepath):
#                 shutil.copy(filepath, os.path.join(target_dir, filename))
#
# source_directory = '/Volumes/Extreme SSD/DataSets/LI/四川甘孜拉萨'
# target_directory = '/Volumes/Extreme SSD/DataSets/LI/四川甘孜拉萨/zanngzu'
# filter_frontal_faces(source_directory, target_directory)
import os
import shutil
import multiprocessing
import face_recognition


def is_frontal_face(image_path):
    image = face_recognition.load_image_file(image_path)

    # 使用face_recognition库进行人脸检测
    face_locations = face_recognition.face_locations(image)

    # 如果有一个以上的脸或没有脸，我们认为它不是正面照片
    if len(face_locations) != 1:
        return False
    return True


def process_directory(directory):
    target_sub_directory = 'frontal_faces'
    target_directory = os.path.join(directory, target_sub_directory)

    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isdir(filepath):
            continue
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')) and is_frontal_face(filepath):
            shutil.copy(filepath, os.path.join(target_directory, filename))


def process_all_directories(root_directory):
    # 获取所有子目录（包括多层子目录）
    directories = [dirpath for dirpath, dirnames, filenames in os.walk(root_directory)]

    # 使用多进程并行处理所有目录
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    pool.map(process_directory, directories)
    pool.close()
    pool.join()


# 使用函数


if __name__ == '__main__':
    multiprocessing.freeze_support()

    # Using the functions
    root_directory = r'D:\races'
    process_all_directories(root_directory)
