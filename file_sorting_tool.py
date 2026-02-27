import os
import re
import shutil
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog, messagebox

INVALID_WINDOWS_CHARS = r'[<>:"/\\|?*]'


@dataclass
class OrganizeStats:
    moved_files: int = 0
    removed_folders: int = 0
    skipped_items: int = 0


def sanitize_name(name: str, fallback: str = "unknown") -> str:
    """Sanitize folder names or file stems for broad filesystem compatibility."""
    sanitized = re.sub(INVALID_WINDOWS_CHARS, "_", name)
    sanitized = sanitized.strip().strip(".")
    return sanitized or fallback


def sanitize_suffix(suffix: str) -> str:
    """Sanitize file suffix while preserving a leading dot."""
    if not suffix:
        return ""
    cleaned = re.sub(INVALID_WINDOWS_CHARS, "_", suffix)
    if not cleaned.startswith("."):
        cleaned = f".{cleaned.lstrip('.')}"
    return cleaned


def unique_destination_path(dest_folder: Path, file_name: str) -> Path:
    """Generate a non-conflicting destination path."""
    base_name = sanitize_name(Path(file_name).stem, fallback="file")
    suffix = sanitize_suffix(Path(file_name).suffix)

    candidate = dest_folder / f"{base_name}{suffix}"
    counter = 1
    while candidate.exists():
        candidate = dest_folder / f"{base_name}_{counter}{suffix}"
        counter += 1
    return candidate


def organize_files_by_user(src_folder: str, dest_folder: str) -> OrganizeStats:
    """Organize files into user folders derived from subfolder naming pattern."""
    src_path = Path(src_folder)
    dest_path = Path(dest_folder)

    if not src_path.exists() or not src_path.is_dir():
        raise ValueError("源文件夹路径不存在或不是文件夹")

    if src_path.resolve() == dest_path.resolve():
        raise ValueError("源文件夹和目标文件夹不能相同")

    dest_path.mkdir(parents=True, exist_ok=True)
    stats = OrganizeStats()

    for subfolder in src_path.iterdir():
        if not subfolder.is_dir():
            stats.skipped_items += 1
            continue

        username_raw = subfolder.name.split(",")[0]
        username = sanitize_name(username_raw, fallback="unknown_user")
        user_dest_folder = dest_path / username
        user_dest_folder.mkdir(parents=True, exist_ok=True)

        for root, _, files in os.walk(subfolder):
            root_path = Path(root)
            for file in files:
                source_file = root_path / file
                destination_file = unique_destination_path(user_dest_folder, file)
                shutil.move(str(source_file), str(destination_file))
                stats.moved_files += 1

        shutil.rmtree(subfolder)
        stats.removed_folders += 1

    return stats


def build_gui() -> tk.Tk:
    root = tk.Tk()
    root.title("文件夹分类工具")

    window_width, window_height = 560, 340
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
    root.resizable(False, False)

    bg_color = "#2b2b2b"
    fg_color = "#ffffff"
    btn_color = "#3c3f41"
    entry_bg_color = "#4e5254"

    root.configure(bg=bg_color)

    def choose_folder(entry: tk.Entry, title: str) -> None:
        folder = filedialog.askdirectory(title=title)
        if folder:
            entry.delete(0, tk.END)
            entry.insert(0, folder)

    def run_organize() -> None:
        src_folder = src_folder_entry.get().strip()
        dest_folder = dest_folder_entry.get().strip()

        if not src_folder or not dest_folder:
            messagebox.showwarning("警告", "请确保已选择源文件夹和目标文件夹！")
            return

        try:
            stats = organize_files_by_user(src_folder, dest_folder)
        except Exception as exc:
            messagebox.showerror("错误", f"文件整理出错：{exc}")
            return

        messagebox.showinfo(
            "完成",
            (
                "文件整理完成！\n"
                f"移动文件数：{stats.moved_files}\n"
                f"清理文件夹数：{stats.removed_folders}\n"
                f"跳过项目数：{stats.skipped_items}"
            ),
        )

    src_label = tk.Label(root, text="源文件夹：", bg=bg_color, fg=fg_color)
    src_label.pack(pady=10)
    src_folder_entry = tk.Entry(
        root,
        width=56,
        bg=entry_bg_color,
        fg=fg_color,
        insertbackground=fg_color,
    )
    src_folder_entry.pack(pady=5)
    src_button = tk.Button(
        root,
        text="选择源文件夹",
        bg=btn_color,
        fg=fg_color,
        command=lambda: choose_folder(src_folder_entry, "选择源文件夹"),
    )
    src_button.pack(pady=5)

    dest_label = tk.Label(root, text="目标文件夹：", bg=bg_color, fg=fg_color)
    dest_label.pack(pady=10)
    dest_folder_entry = tk.Entry(
        root,
        width=56,
        bg=entry_bg_color,
        fg=fg_color,
        insertbackground=fg_color,
    )
    dest_folder_entry.pack(pady=5)
    dest_button = tk.Button(
        root,
        text="选择目标文件夹",
        bg=btn_color,
        fg=fg_color,
        command=lambda: choose_folder(dest_folder_entry, "选择目标文件夹"),
    )
    dest_button.pack(pady=5)

    start_button = tk.Button(root, text="开始整理", bg=btn_color, fg=fg_color, command=run_organize)
    start_button.pack(pady=20)

    return root


if __name__ == "__main__":
    app = build_gui()
    app.mainloop()
