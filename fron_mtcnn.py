import os
import numpy as np
import cv2
from facenet_pytorch import MTCNN
import shutil, torch


def is_frontal_face(landmarks):
    """判断脸部是否正面"""
    left_eye = landmarks[0]
    right_eye = landmarks[1]
    a = np.array([left_eye[0], left_eye[1], right_eye[0], right_eye[1]])
    print(a)
    if np.sum(a == 0) == 0:
        return True
    else:
        return False


def read_image_using_np_fromfile(file_path):
    """使用np.fromfile读取图像并用cv2.imdecode解码"""
    img_data = np.fromfile(file_path, dtype=np.uint8)
    img = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
    return img


def filter_frontal_faces(input_dir, output_subdir_name):
    """处理文件夹内的所有图像，并筛选出正面脸部图像"""

    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    mtcnn = MTCNN(keep_all=True, device=device)

    all_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(input_dir) for f in filenames if
                 f.lower().endswith(('png', 'jpg', 'jpeg'))]

    for file_path in all_files:
        img = read_image_using_np_fromfile(file_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        _, _, landmarks = mtcnn.detect(img_rgb, landmarks=True)

        if landmarks is not None:
            for landmark in landmarks:
                if is_frontal_face(landmark):
                    dest_folder = os.path.join(os.path.dirname(file_path), output_subdir_name)
                    if not os.path.exists(dest_folder):
                        os.makedirs(dest_folder)
                    shutil.copy(file_path, os.path.join(dest_folder, os.path.basename(file_path)))
                    print("FIND:", os.path.join(dest_folder, os.path.basename(file_path)))
                    break


if __name__ == '__main__':
    input_directory = r"D:\races\tests\新建文件夹"
    output_subdir_name = "selected"  # 这将在每个图片所在的文件夹内创建一个名为 "selected" 的子目录
    filter_frontal_faces(input_directory, output_subdir_name)
