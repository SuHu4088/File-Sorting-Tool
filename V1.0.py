import os
import shutil

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
                    
                    # 移动文件到目标文件夹中
                    shutil.move(file_path, user_dest_folder)

            # 删除已处理的子文件夹
            shutil.rmtree(subfolder_path)

if __name__ == "__main__":
    # 指定源文件夹和目标文件夹路径
    src_folder = r"~:\~~"  # 替换为你的源文件夹路径
    dest_folder = r"~:\~~\整理后的文件"  # 替换为你的目标文件夹路径

    # 调用函数
    organize_files_by_user(src_folder, dest_folder)
    print("文件整理完成！")
