import os
import shutil
from pathlib import Path

def organize_files_by_user(src_folder, dest_folder):
    # 创建目标文件夹
    os.makedirs(dest_folder, exist_ok=True)

    # 遍历源文件夹中的子文件夹
    for subfolder in os.listdir(src_folder):
        subfolder_path = os.path.join(src_folder, subfolder)
        
        if os.path.isdir(subfolder_path):
            # 提取用户名（第一个逗号之前的部分）
            username = subfolder.split(",")[0]
            user_dest_folder = os.path.join(dest_folder, username)
            os.makedirs(user_dest_folder, exist_ok=True)

            # 遍历子文件夹中的文件
            for root, _, files in os.walk(subfolder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    dest_file_path = os.path.join(user_dest_folder, file)

                    # 如果目标路径中已有文件，则重命名
                    if os.path.exists(dest_file_path):
                        base, extension = os.path.splitext(file)
                        counter = 1
                        # 找到一个新的不冲突的文件名
                        while os.path.exists(dest_file_path):
                            new_file_name = f"{base}_{counter}{extension}"
                            dest_file_path = os.path.join(user_dest_folder, new_file_name)
                            counter += 1
                    
                    # 移动文件
                    shutil.move(file_path, dest_file_path)

            # 删除已处理的子文件夹
            shutil.rmtree(subfolder_path)

if __name__ == "__main__":
    # 直接指定路径
    src_folder = "F:/测试/整理后的文件"  # 替换为实际的源文件夹路径
    dest_folder = "F:/测试/整理后的文件"  # 替换为实际的目标文件夹路径

    # 调用函数
    organize_files_by_user(src_folder, dest_folder)
    print("文件整理完成！")
