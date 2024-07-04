import os
import shutil
import base_path as bp

# 定义路径
dataset_directory = bp.dataset_path
train_directory = os.path.join(dataset_directory, 'train')
test_directory = os.path.join(dataset_directory, 'test')

def clear_directory(directory):
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

def copy_folder_contents(src_folder, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    for item in os.listdir(src_folder):
        src_path = os.path.join(src_folder, item)
        dest_path = os.path.join(dest_folder, item)
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dest_path)
        else:
            shutil.copy2(src_path, dest_path)
        print(f"Copied {src_path} to {dest_path}")

# 清空 test 目录
clear_directory(test_directory)

# 定义需要复制的子文件夹
subfolders = ['clean', 'ripple']

for subfolder in subfolders:
    src_folder = os.path.join(train_directory, subfolder)
    dest_folder = os.path.join(test_directory, subfolder)
    copy_folder_contents(src_folder, dest_folder)
