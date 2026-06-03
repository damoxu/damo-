tags: 技术
project: 静态博客项目
# build.py 解析：博客的构建引擎

> 整个博客的核心就是这一个文件，约 150 行，负责把 Markdown 变成网站。

---

## 它做了什么

```
你写的 .md 文件
      ↓
读取文件内容
      ↓
解析头部元数据（title / date / tags）
      ↓
正文转成 HTML
      ↓
填入 Jinja2 模板
      ↓
写到 output/ 目录
```

每次运行 `python build.py`，就完成了以上全部步骤。

---

## 文件结构

```python
# 1. 配置区
#    BLOG_TITLE、AUTHOR_NAME、BASE_URL 等
#    整个项目只需要改这里

# 2. 工具函数
#    read_markdown_file()   读取并解析一个 .md 文件
#    collect_all_posts()    扫描 content/posts/ 收集所有文章
#    collect_all_works()    扫描 content/works/ 收集所有作品

# 3. 渲染函数
#    setup_jinja()          初始化模板引擎
#    render_page()          把数据填进模板，输出 HTML 文件

# 4. 构建流程
#    clean_output_dir()     清空 output/ 目录
#    copy_static_files()    复制 CSS、图片
#    build_search_index()   生成搜索索引 JSON
#    build()                主函数，按顺序调用以上所有步骤

# 5. 入口
#    if __name__ == "__main__": build()
```

---

## 核心函数详解

### read_markdown_file()

```python
def read_markdown_file(filepath):
    with open(filepath, encoding="utf-8") as f:
        raw_text = f.read()

    md = markdown.Markdown(extensions=["meta", "fenced_code", "tables"])
    html_body = md.convert(raw_text)

    meta = {key: values[0] for key, values in md.Meta.items()}
    return meta, html_body
```

**做了两件事：**
- 把 Markdown 正文转成 HTML
- 把头部的 `title:`、`date:`、`tags:` 提取出来

### render_page()

```python
def render_page(env, template_name, output_path, **data):
    template = env.get_template(template_name)
    html = template.render(**data, blog_title=BLOG_TITLE, author=AUTHOR_NAME, base_url=BASE_URL)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
```

**通用渲染函数：** 传入模板名、输出路径、数据，输出一个 HTML 文件。

---

## 构建顺序

```
步骤 1   清空 output/
步骤 2   复制 static/ → output/static/
步骤 3   生成每篇文章页面  → output/posts/*.html
步骤 4   生成每个作品页面  → output/works/*.html
步骤 5   生成作品集列表页  → output/works/index.html
步骤 6   生成首页          → output/index.html
步骤 7   生成搜索索引      → output/search-index.json
步骤 8   生成搜索页        → output/search.html
```

---

## 日常使用

```bash
python build.py
```

看到 `✅ 构建完成` 就说明一切正常。