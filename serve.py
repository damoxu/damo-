# serve.py
# 作用：本地预览博客，每次修改文章后自动重新构建
#
# 使用方法：
#   python serve.py
# 然后打开浏览器访问 http://localhost:8000

import os
import time
import threading
import http.server
import webbrowser
from build import build

# ─────────────────────────────────────────
# 配置
# ─────────────────────────────────────────

PORT         = 8000
WATCH_DIRS   = ["content", "templates", "static"]  # 监听这些目录的变化
OUTPUT_DIR   = "output"
CHECK_INTERVAL = 1  # 每隔多少秒检查一次文件变化（秒）


# ─────────────────────────────────────────
# 文件变化检测
# ─────────────────────────────────────────

def get_all_files_with_mtime(dirs):
    """
    扫描指定目录下所有文件，返回一个字典：
    { 文件路径: 最后修改时间 }
    """
    files = {}
    for directory in dirs:
        if not os.path.exists(directory):
            continue
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                files[filepath] = os.path.getmtime(filepath)
    return files


def has_any_file_changed(old_snapshot, new_snapshot):
    """
    对比两次文件快照，判断是否有文件被新增、删除或修改。
    """
    # 有文件被新增或删除
    if set(old_snapshot.keys()) != set(new_snapshot.keys()):
        return True

    # 有文件的修改时间变了
    for filepath, mtime in new_snapshot.items():
        if old_snapshot.get(filepath) != mtime:
            return True

    return False


# ─────────────────────────────────────────
# 自动重建监听器
# ─────────────────────────────────────────

def watch_and_rebuild():
    """
    在后台持续监听文件变化。
    一旦检测到变化，立刻重新构建博客。
    """
    print(f"👀 监听文件变化中：{WATCH_DIRS}")
    snapshot = get_all_files_with_mtime(WATCH_DIRS)

    while True:
        time.sleep(CHECK_INTERVAL)
        new_snapshot = get_all_files_with_mtime(WATCH_DIRS)

        if has_any_file_changed(snapshot, new_snapshot):
            print("\n📄 检测到文件变化，重新构建...")
            build()
            snapshot = new_snapshot


# ─────────────────────────────────────────
# 本地 HTTP 服务器
# ─────────────────────────────────────────

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    """
    继承标准 HTTP 处理器，只关掉每次请求的日志输出，
    让终端不被刷屏，只显示构建信息。
    """

    def __init__(self, *args, **kwargs):
        # 指定从 output/ 目录提供文件
        super().__init__(*args, directory=OUTPUT_DIR, **kwargs)

    def log_message(self, format, *args):
        pass  # 不打印每条请求日志


# ─────────────────────────────────────────
# 主函数：启动服务器 + 启动监听器
# ─────────────────────────────────────────

def main():
    # 先构建一次，确保 output/ 是最新的
    build()

    # 在后台线程里启动文件监听器
    watcher_thread = threading.Thread(target=watch_and_rebuild, daemon=True)
    watcher_thread.start()

    # 启动本地服务器
    server = http.server.HTTPServer(("", PORT), QuietHandler)
    url = f"http://localhost:{PORT}"
    print(f"🌐 本地预览：{url}")
    print("   按 Ctrl+C 停止\n")

    # 自动在浏览器里打开
    webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")


if __name__ == "__main__":
    main()