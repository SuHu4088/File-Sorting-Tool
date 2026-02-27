"""兼容入口：保留旧文件名，实际功能迁移到 file_sorting_tool.py。"""

from file_sorting_tool import build_gui


if __name__ == "__main__":
    app = build_gui()
    app.mainloop()
