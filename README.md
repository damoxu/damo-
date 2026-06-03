# 静态博客

用 Python + Markdown 构建的个人博客，支持文章、作品集、全文搜索。

## 项目结构

​```
my-blog/
├── content/          # 内容目录
│   ├── posts/        # 文章（.md 文件）
│   └── works/        # 作品集（.md 文件）
├── templates/        # HTML 模板
│   ├── base.html     # 公共骨架（导航、页脚）
│   ├── index.html    # 首页
│   ├── post.html     # 文章详情页
│   ├── work.html     # 作品详情页
│   └── search.html   # 搜索页
├── static/
│   └── style.css     # 样式
├── output/           # 构建产物（自动生成，不要手动修改）
├── build.py          # 构建脚本
└── serve.py          # 本地预览服务器
​```

## 快速开始

安装依赖：

​```bash
pip install markdown jinja2
​```

本地预览：

​```bash
python serve.py
# 打开 http://localhost:8000
​```

构建并发布：

​```bash
python build.py
git add .
git commit -m "new post"
git push
​```

## 写文章

在 `content/posts/` 下新建 `.md` 文件，格式如下：

​```markdown
title: 文章标题
date: 2024-01-01
tags: 标签一, 标签二

## 正文从这里开始

支持标准 Markdown 语法。
​```

## 写作品

在 `content/works/` 下新建 `.md` 文件：

​```markdown
title: 作品名称
desc: 一句话描述
link: https://github.com/你的用户名/项目

## 详细介绍

这里写作品的详细说明。
​```

## 技术栈

| 用途 | 选择 |
|------|------|
| 构建脚本 | Python 3 |
| Markdown 解析 | markdown 库 |
| 模板引擎 | Jinja2 |
| 样式 | 纯 CSS |
| 部署 | GitHub Pages + Actions |

## 在线地址

https://damoxu.github.io/damo-/