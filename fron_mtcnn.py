import os
import numpy as np
import cv2
from facenet_pytorch import MTCNN
import torch
import shutil
from multiprocessing import Pool, cpu_count


def is_frontal_face(landmarks):
    """判断脸部是否正面"""
    left_eye = landmarks[0]
    right_eye = landmarks[1]
    nose = landmarks[2]
    left_mouth = landmarks[3]
    right_mouth = landmarks[4]

    eye_dx = right_eye[0] - left_eye[0]
    eye_dy = right_eye[1] - left_eye[1]

    # Calculate the angle between the eyes
    angle = -np.arctan2(eye_dy, eye_dx) * 180. / np.pi

    # Check for frontal face
    return -10 <= angle <= 10


def read_image_using_np_fromfile(file_path):
    """使用np.fromfile读取图像并用cv2.imdecode解码"""
    img_data = np.fromfile(file_path, dtype=np.uint8)
    img = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
    return img


def filter_frontal_faces_process(args):
    files, output_subdir_name = args
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    mtcnn = MTCNN(keep_all=True, device=device)

    # mtcnn = MTCNN(keep_all=True, device='cuda:0')  # 使用GPU

    for file_path in files:
        # 使用np.fromfile和cv2.imdecode读取图像
        img = read_image_using_np_fromfile(file_path)

        # 将BGR格式的图像转为RGB格式
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # MTCNN检测
        _, _, landmarks = mtcnn.detect(img_rgb, landmarks=True)

        if landmarks is not None:
            for landmark in landmarks:
                if is_frontal_face(landmark):
                    dest_folder = os.path.join(os.path.dirname(file_path), output_subdir_name)
                    if not os.path.exists(dest_folder):
                        os.makedirs(dest_folder)
                    shutil.copy(file_path, os.path.join(dest_folder, os.path.basename(file_path)))
                    print(os.path.join(dest_folder, os.path.basename(file_path)))
                    break


def filter_frontal_faces(input_dir, output_subdir_name, num_processes=None):
    """处理文件夹内的所有图像，并筛选出正面脸部图像"""
    if num_processes is None:
        num_processes = cpu_count()

    # 获取所有图像路径
    all_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(input_dir) for f in filenames if
                 f.lower().endswith(('png', 'jpg', 'jpeg'))]
    split_files = [all_files[i::num_processes] for i in range(num_processes)]

    # 使用多进程进行处理
    with Pool(num_processes) as pool:
        pool.map(filter_frontal_faces_process, [(files, output_subdir_name) for files in split_files])


if __name__ == '__main__':
    input_directory = r"D:\races\tests"
    output_subdir_name = "selected"  # 这将在每个图片所在的文件夹内创建一个名为 "selected" 的子目录
    filter_frontal_faces(input_directory, output_subdir_name, 2)
