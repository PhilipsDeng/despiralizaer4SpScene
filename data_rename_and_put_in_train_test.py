import os
import shutil
import random
import base_path as bp

# 定义路径
org_data_directory = bp.org_data_path
dataset_directory = bp.dataset_path

def rename_files_in_subfolders(base_directory, prefix):
    for folder in os.listdir(base_directory):
        folder_path = os.path.join(base_directory, folder)
        if os.path.isdir(folder_path):
            rename_files(folder_path, prefix)

def rename_files(directory, prefix):
    for root, dirs, files in os.walk(directory):
        for idx, filename in enumerate(sorted(files)):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                old_path = os.path.join(root, filename)
                new_filename = f"{prefix}_{idx:05d}.png"
                new_path = os.path.join(root, new_filename)
                os.rename(old_path, new_path)
                print(f"Renamed {old_path} to {new_path}")

# 重命名所有子文件夹中的图像
rename_files_in_subfolders(org_data_directory, "image")

# 定义你的基目录和目标目录
ripple_directory = os.path.join(dataset_directory, 'ripple')
clean_directory = os.path.join(dataset_directory, 'clean')
train_directory = os.path.join(dataset_directory, 'train')
test_directory = os.path.join(dataset_directory, 'test')

# 如果目标目录不存在，则创建它们
os.makedirs(ripple_directory, exist_ok=True)
os.makedirs(clean_directory, exist_ok=True)
os.makedirs(train_directory, exist_ok=True)
os.makedirs(test_directory, exist_ok=True)

def copy_and_rename_files(src_folder, dest_folder, prefix, start_idx):
    files = sorted(os.listdir(src_folder))
    for idx, filename in enumerate(files):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            old_path = os.path.join(src_folder, filename)
            new_filename = f"{prefix}{start_idx + idx:05d}.png"
            new_path = os.path.join(dest_folder, new_filename)
            shutil.copy(old_path, new_path)
            print(f"Copied and renamed {old_path} to {new_path}")
    return start_idx + len(files)

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

def copy_files_to_train_test(src_folder, prefix, train_range, test_range):
    files = sorted([f for f in os.listdir(src_folder) if f.endswith(('.png', '.jpg', '.jpeg'))])
    train_folder = os.path.join(train_directory, prefix)
    test_folder = os.path.join(test_directory, prefix)
    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(test_folder, exist_ok=True)
    
    for idx, filename in enumerate(files):
        old_path = os.path.join(src_folder, filename)
        if idx in train_range:
            new_path = os.path.join(train_folder, filename)
        elif idx in test_range:
            new_path = os.path.join(test_folder, filename)
        shutil.copy(old_path, new_path)
        print(f"Copied {old_path} to {new_path}")

# 获取所有文件夹
folders = os.listdir(org_data_directory)

# 初始化序号
ripple_start_idx = 0
clean_start_idx = 0

clear_directory(ripple_directory)
clear_directory(clean_directory)
clear_directory(train_directory)
clear_directory(test_directory)

for folder in folders:
    folder_path = os.path.join(org_data_directory, folder)
    if os.path.isdir(folder_path):
        if folder.endswith('_test'):
            ripple_start_idx = copy_and_rename_files(folder_path, ripple_directory, 'ripple', ripple_start_idx)
        elif folder.endswith('_test_gt'):
            clean_start_idx = copy_and_rename_files(folder_path, clean_directory, 'clean', clean_start_idx)

# 手动输入区间，将区间内的图片放入train文件夹，其余放入test文件夹
def input_train_test_ranges():
    ranges = input("请输入训练集区间(0-99,60,50%)：")
    train_range = set()
    test_range = set()
    
    # 获取文件总数
    total_files = len(os.listdir(ripple_directory))
    
    for part in ranges.split(','):
        if part.endswith('%'):
            # 处理百分比
            percentage = int(part[:-1])
            num_files = total_files * percentage // 100
            train_range.update(random.sample(range(total_files), num_files))
        elif '-' in part:
            # 处理区间范围
            start, end = map(int, part.split('-'))
            train_range.update(range(start, end + 1))
        else:
            # 处理具体数量
            num_files = int(part)
            train_range.update(range(num_files))
    
    # 计算测试集
    test_range.update(set(range(total_files)) - train_range)
    
    return train_range, test_range


# 新增函数：打乱两个文件夹的文件顺序
def shuffle_files(folder1, folder2):
    files1 = sorted([f for f in os.listdir(folder1) if f.endswith(('.png', '.jpg', '.jpeg'))])
    files2 = sorted([f for f in os.listdir(folder2) if f.endswith(('.png', '.jpg', '.jpeg'))])
    
    if len(files1) != len(files2):
        raise ValueError("两个文件夹中的文件数量不一致")
    
    combined = list(zip(files1, files2))
    random.shuffle(combined)
    
    for idx, (file1, file2) in enumerate(combined):
        old_path1 = os.path.join(folder1, file1)
        new_path1 = os.path.join(folder1, f"img{idx:05d}.png")
        old_path2 = os.path.join(folder2, file2)
        new_path2 = os.path.join(folder2, f"img{idx:05d}.png")
        
        os.rename(old_path1, new_path1)
        os.rename(old_path2, new_path2)
        
        print(f"Renamed {old_path1} to {new_path1}")
        print(f"Renamed {old_path2} to {new_path2}")

# 将图片复制到train和test文件夹中
ripple_train_range, ripple_test_range = input_train_test_ranges()
clean_train_range, clean_test_range = ripple_train_range, ripple_test_range

# 打乱文件夹中的文件顺序
shuffle_files(ripple_directory, clean_directory)

# 确保 clean 和 ripple 对应的文件保持一致
copy_files_to_train_test(ripple_directory, 'ripple', ripple_train_range, ripple_test_range)
copy_files_to_train_test(clean_directory, 'clean', clean_train_range, clean_test_range)
