# build.py
# 作用：把 content/ 里的 Markdown 文件，转成 output/ 里的 HTML 文件

import os
import shutil
import markdown
from jinja2 import Environment, FileSystemLoader
from datetime import date

# ─────────────────────────────────────────
# 1. 配置：整个项目只有这里需要改
# ─────────────────────────────────────────

BLOG_TITLE  = "我的博客"
AUTHOR_NAME = "damoxu"

DIR_CONTENT   = "content"    # Markdown 文章放这里
DIR_TEMPLATES = "templates"  # HTML 模板放这里
DIR_STATIC    = "static"     # CSS / 图片放这里
DIR_OUTPUT    = "output"     # 生成结果放这里
BASE_URL = "/damo-"   # 部署到子目录时的前缀，本地预览留空即可

# ─────────────────────────────────────────
# 2. 工具函数：每个函数只做一件事
# ─────────────────────────────────────────

def read_markdown_file(filepath):
    """
    读取一个 Markdown 文件，返回：
    - meta : 文章头部信息（标题、日期、标签）
    - html : 正文转成的 HTML 字符串
    """
    with open(filepath, encoding="utf-8") as f:
        raw_text = f.read()

    # markdown 库同时处理正文和头部元数据
    md = markdown.Markdown(extensions=["meta", "fenced_code", "tables"])
    html_body = md.convert(raw_text)

    # md.Meta 里的值是列表，取第一个元素变成字符串
    meta = {key: values[0] for key, values in md.Meta.items()}
    return meta, html_body


def collect_all_posts(posts_dir):
    """
    扫描 content/posts/ 目录，收集所有文章信息。
    返回一个列表，每项是一篇文章的字典。
    """
    posts = []

    for filename in sorted(os.listdir(posts_dir), reverse=True):
        if not filename.endswith(".md"):
            continue  # 跳过非 Markdown 文件

        filepath = os.path.join(posts_dir, filename)
        meta, html_body = read_markdown_file(filepath)
        # 没有填 title 就用文件名（去掉 .md 后缀）
        title = meta.get("title", "").strip()
        if not title:
            title = filename.replace(".md", "")

        # 没有填 date 就用今天的日期
        date_str = meta.get("date", "").strip()
        if not date_str:
            date_str = date.today().strftime("%Y-%m-%d")

        # 没有填 tags 就留空列表
        tags_str = meta.get("tags", "").strip()
        tags = tags_str.split(",") if tags_str else []
        post = {
            "slug"  : filename.replace(".md", ""),
            "title" : title,
            "date"  : date_str,
            "tags"  : tags,
            "body"  : html_body,
            "url"   : f"posts/{filename.replace('.md', '.html')}",
        }
        posts.append(post)

    return posts


def collect_all_works(works_dir):
    """
    扫描 content/works/ 目录，收集所有作品信息。
    逻辑和 collect_all_posts 一样，单独分开方便以后扩展。
    """
    works = []

    for filename in sorted(os.listdir(works_dir)):
        if not filename.endswith(".md"):
            continue

        filepath = os.path.join(works_dir, filename)
        meta, html_body = read_markdown_file(filepath)

        # 没有填 title 就用文件名
        title = meta.get("title", "").strip()
        if not title:
            title = filename.replace(".md", "")

        work = {
            "slug"  : filename.replace(".md", ""),
            "title" : title,
            "desc"  : meta.get("desc",  ""),
            "link"  : meta.get("link",  "#"),
            "body"  : html_body,
            "url"   : f"works/{filename.replace('.md', '.html')}",
        }
        works.append(work)

    return works


# ─────────────────────────────────────────
# 3. 渲染函数：把数据填进模板，生成 HTML
# ─────────────────────────────────────────

def setup_jinja(templates_dir):
    """初始化 Jinja2 模板引擎，告诉它去哪里找模板文件。"""
    env = Environment(loader=FileSystemLoader(templates_dir))
    return env


def render_page(env, template_name, output_path, **data):
    """
    通用渲染函数：
    - env           : Jinja2 引擎
    - template_name : 用哪个模板（如 "post.html"）
    - output_path   : 输出到哪里（如 "output/posts/my-post.html"）
    - **data        : 传给模板的所有变量
    """
    template = env.get_template(template_name)
    html = template.render(**data, blog_title=BLOG_TITLE, author=AUTHOR_NAME, base_url=BASE_URL)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  ✓ 生成：{output_path}")


# ─────────────────────────────────────────
# 4. 构建流程：按顺序执行每一步
# ─────────────────────────────────────────

def clean_output_dir():
    """清空 output/ 目录，确保每次构建都是干净的。"""
    if os.path.exists(DIR_OUTPUT):
        shutil.rmtree(DIR_OUTPUT)
    os.makedirs(DIR_OUTPUT)


def copy_static_files():
    """把 static/ 里的 CSS、图片原样复制到 output/static/。"""
    src = DIR_STATIC
    dst = os.path.join(DIR_OUTPUT, "static")
    shutil.copytree(src, dst)
    print(f"  ✓ 复制静态文件：{src} → {dst}")
def build_search_index(posts, works, output_dir):
    """
    把所有文章和作品的标题、正文提取出来，
    生成一个 JSON 文件供前端搜索使用。
    """
    import json
    import re

    index = []

    for post in posts:
        # 把 HTML 标签去掉，只保留纯文字
        plain_text = re.sub(r"<[^>]+>", "", post["body"])
        index.append({
            "title" : post["title"],
            "date"  : post["date"],
            "tags"  : post["tags"],
            "url"   : "/" + post["url"],
            "body"  : plain_text[:500],   # 只取前500字，节省体积
            "type"  : "post",
        })

    for work in works:
        plain_text = re.sub(r"<[^>]+>", "", work["body"])
        index.append({
            "title" : work["title"],
            "desc"  : work["desc"],
            "url"   : "/" + work["url"],
            "body"  : plain_text[:500],
            "type"  : "work",
        })

    # 写入 JSON 文件
    index_path = os.path.join(output_dir, "search-index.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"  ✓ 生成搜索索引：{index_path}")

def build():
    """
    主构建函数，按顺序做这几件事：
    1. 清空输出目录
    2. 复制静态文件
    3. 收集所有文章和作品
    4. 为每篇文章生成独立 HTML 页面
    5. 为每个作品生成独立 HTML 页面
    6. 生成首页
    """
    print("\n🔨 开始构建...\n")

    # 步骤 1 & 2
    clean_output_dir()
    copy_static_files()

    # 步骤 3：收集内容
    posts = collect_all_posts(os.path.join(DIR_CONTENT, "posts"))
    works = collect_all_works(os.path.join(DIR_CONTENT, "works"))

    env = setup_jinja(DIR_TEMPLATES)

    # 步骤 4：每篇文章单独生成一个 HTML 页面
    print("\n📝 生成文章页面：")
    for post in posts:
        output_path = os.path.join(DIR_OUTPUT, post["url"])
        render_page(env, "post.html", output_path, post=post)

    # 步骤 5：每个作品单独生成一个 HTML 页面
    print("\n🎨 生成作品页面：")
    for work in works:
        output_path = os.path.join(DIR_OUTPUT, work["url"])
        render_page(env, "work.html", output_path, work=work)

    # 步骤 6：生成首页（把文章列表和作品列表都传进去）
    print("\n🏠 生成首页：")
    render_page(env, "index.html",
                os.path.join(DIR_OUTPUT, "index.html"),
                posts=posts,
                works=works)
    #步骤 7：生成搜索索引
    print("\n🔍 生成搜索索引：")
    build_search_index(posts, works, DIR_OUTPUT)
    # 步骤 8：生成搜索页
    print("\n🔍 生成搜索页：")
    render_page(env, "search.html",
                os.path.join(DIR_OUTPUT, "search.html"),
                posts=posts,
                works=works)


    print("\n✅ 构建完成！打开 output/index.html 查看结果。\n")


# ─────────────────────────────────────────
# 5. 入口：直接运行这个文件时执行构建
# ─────────────────────────────────────────

if __name__ == "__main__":
    build()
