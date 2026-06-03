project: 静态博客生成器
# serve.py 解析：本地预览服务器

> 改完文章不用每次手动下载文件，直接在浏览器里看效果。

---

## 使用方法

```bash
python serve.py
# 然后打开浏览器访问 http://localhost:8000
```

修改 `content/`、`templates/`、`static/` 里的任何文件，会自动重新构建，刷新浏览器即可看到最新效果。

按 `Ctrl + C` 停止服务器。

---

## 它做了什么

```
启动时
  ↓
先构建一次，确保 output/ 是最新的
  ↓
启动后台线程：每隔 1 秒扫描文件变化
  ↓
启动 HTTP 服务器，提供 output/ 里的文件
  ↓
浏览器访问 http://localhost:8000 → 看到博客
```

---

## 文件结构

```python
# 1. 配置
#    PORT = 8000
#    WATCH_DIRS = ["content", "templates", "static"]
#    CHECK_INTERVAL = 1  # 每秒检查一次

# 2. 文件变化检测
#    get_all_files_with_mtime()   扫描目录，记录每个文件的修改时间
#    has_any_file_changed()       对比两次快照，判断是否有变化

# 3. 自动重建监听器
#    watch_and_rebuild()          后台线程，检测到变化就重新构建

# 4. HTTP 服务器
#    QuietHandler                 继承标准服务器，关掉请求日志

# 5. 主函数
#    main()                       启动服务器 + 启动监听器
```

---

## 核心机制：文件快照对比

```python
# 第一次扫描，记录所有文件的修改时间
snapshot = {"content/posts/hello.md": 1717392000.0, ...}

# 1 秒后再扫描
new_snapshot = {"content/posts/hello.md": 1717392060.0, ...}

# 修改时间不一样 → 触发重新构建
```

这个方法简单可靠，不依赖任何额外的库。

---

## 注意事项

服务器环境没有浏览器，`webbrowser.open()` 会报警告，忽略即可，不影响使用。

本地预览和线上部署的路径不同（线上有 `/damo-/` 前缀），所以本地预览时链接跳转可能有问题，以线上为准。