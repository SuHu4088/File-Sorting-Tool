import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def organize_files_by_user(src_folder, dest_folder):
    try:
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

        messagebox.showinfo("完成", "文件整理完成！结果已保存到目标文件夹。")
    except Exception as e:
        messagebox.showerror("错误", f"文件整理出错：{str(e)}")

def choose_src_folder():
    folder = filedialog.askdirectory(title="选择源文件夹")
    if folder:
        src_folder_entry.delete(0, tk.END)
        src_folder_entry.insert(0, folder)

def choose_dest_folder():
    folder = filedialog.askdirectory(title="选择目标文件夹")
    if folder:
        dest_folder_entry.delete(0, tk.END)
        dest_folder_entry.insert(0, folder)

def run_organize():
    src_folder = src_folder_entry.get().strip()
    dest_folder = dest_folder_entry.get().strip()
    if not src_folder or not dest_folder:
        messagebox.showwarning("警告", "请确保已选择源文件夹和目标文件夹！")
        return
    if not os.path.exists(src_folder):
        messagebox.showerror("错误", "源文件夹路径不存在！")
        return
    organize_files_by_user(src_folder, dest_folder)

# 创建 GUI
root = tk.Tk()
root.title("文件夹分类工具")

# 居中屏幕
window_width, window_height = 500, 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
root.resizable(False, False)

# 设置暗黑配色
bg_color = "#2b2b2b"
fg_color = "#ffffff"
btn_color = "#3c3f41"
entry_bg_color = "#4e5254"

root.configure(bg=bg_color)

# GUI布局
# 源文件夹选择
src_label = tk.Label(root, text="源文件夹：", bg=bg_color, fg=fg_color)
src_label.pack(pady=10)
src_folder_entry = tk.Entry(root, width=50, bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
src_folder_entry.pack(pady=5)
src_button = tk.Button(root, text="选择源文件夹", bg=btn_color, fg=fg_color, command=choose_src_folder)
src_button.pack(pady=5)

# 目标文件夹选择
dest_label = tk.Label(root, text="目标文件夹：", bg=bg_color, fg=fg_color)
dest_label.pack(pady=10)
dest_folder_entry = tk.Entry(root, width=50, bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
dest_folder_entry.pack(pady=5)
dest_button = tk.Button(root, text="选择目标文件夹", bg=btn_color, fg=fg_color, command=choose_dest_folder)
dest_button.pack(pady=5)

# 开始按钮
start_button = tk.Button(root, text="开始整理", bg=btn_color, fg=fg_color, command=run_organize)
start_button.pack(pady=20)

# 运行主循环
root.mainloop()
