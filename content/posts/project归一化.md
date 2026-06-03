project: 静态博客生成器
作品集里面可不可以有很多文章?

可以，作品集里的每个作品本身就是一篇 `.md` 文件，可以写很长的内容。

**情况一：一个作品下面挂多篇文章** 比如"静态博客项目"这个作品，下面有"build.py解析"、"模板解析"、"部署解析"几篇子文章。

**情况二：作品集页面像文章列表一样，显示很多条目** 现在已经支持了，`content/works/` 里有几个 `.md` 就显示几个卡片。

**情况三：文章可以归属到某个作品/项目下** 比如给文章加一个 `project: 静态博客` 字段，首页按项目分组显示。

明白了，你是说一篇文章可以同时属于某个作品，比如：

```
作品：静态博客项目
  └── build.py 解析
  └── 模板系统解析
  └── 搜索功能解析
```

想在作品页里能看到相关文章列表，文章页也能看到"所属项目"。

实现方式是给文章加一个 `project` 字段：

markdown

```markdown
title: build.py 解析
date: 2026-06-03
tags: 技术
project: 静态博客项目    ← 加这一行
```

然后 `build.py` 收集文章时把这个字段读出来，作品页模板里过滤出相关文章显示。

要做吗？我来带你改 `build.py` 和模板。

嗯好

19:34

分三步来做。

------

### 第一步：改 `build.py` 读取 `project` 字段

bash

```bash
nano build.py
```

找到 `collect_all_posts` 函数里的 `post = {` 这段，加一行 `project`：

python

```python
        post = {
            "slug"    : filename.replace(".md", ""),
            "title"   : title,
            "date"    : date_str,
            "tags"    : tags,
            "project" : meta.get("project", "").strip(),  # ← 加这行
            "body"    : html_body,
            "url"     : f"posts/{filename.replace('.md', '.html')}",
        }
```

------

### 第二步：改 `work.html` 模板，显示相关文章

bash

```bash
nano templates/work.html
```

把整个文件改成：

html

```html
{% extends "base.html" %}

{% set page_title = work.title %}

{% block content %}

  <article class="post">

    <header class="post-header">
      <h1 class="post-title">{{ work.title }}</h1>
      {% if work.link != "#" %}
        <a href="{{ work.link }}" class="work-link" target="_blank">查看项目 →</a>
      {% endif %}
    </header>

    <div class="post-body">
      {{ work.body | safe }}
    </div>

    <!-- 相关文章：title 里包含作品名，或 project 字段匹配的文章 -->
    {% set related = [] %}
    {% for post in posts %}
      {% if post.project == work.title %}
        {% set _ = related.append(post) %}
      {% endif %}
    {% endfor %}

    {% if related %}
    <div class="related-posts">
      <h3 class="related-title">相关文章</h3>
      <ul class="post-list">
        {% for post in related %}
          <li class="post-list-item">
            <a href="{{ base_url }}/{{ post.url }}" class="post-list-title">{{ post.title }}</a>
            <span class="post-list-date">{{ post.date }}</span>
          </li>
        {% endfor %}
      </ul>
    </div>
    {% endif %}

    <footer class="post-footer">
      <a href="{{ base_url }}/index.html">← 返回首页</a>
    </footer>

  </article>

{% endblock %}
```

------

### 第三步：改 `post.html`，显示所属项目

bash

```bash
nano templates/post.html
```

在 `post-meta` 那段加所属项目的显示：

html

```html
    <header class="post-header">
      <h1 class="post-title">{{ post.title }}</h1>
      <div class="post-meta">
        <span class="post-date">{{ post.date }}</span>
        {% for tag in post.tags %}
          <span class="post-tag">{{ tag.strip() }}</span>
        {% endfor %}
        {% if post.project %}
          <a href="{{ base_url }}/works/" class="post-project">
            📁 {{ post.project }}
          </a>
        {% endif %}
      </div>
    </header>
```

------

### 第四步：让 `render_page` 把 `posts` 传给作品页

bash

```bash
nano build.py
```

找到生成作品页那段：

python

```python
    for work in works:
        output_path = os.path.join(DIR_OUTPUT, work["url"])
        render_page(env, "work.html", output_path, work=work)
```

改成：

python

```python
    for work in works:
        output_path = os.path.join(DIR_OUTPUT, work["url"])
        render_page(env, "work.html", output_path, work=work, posts=posts)
```

------

### 第五步：加样式

bash

```bash
nano static/style.css
```

在最底部加：

css

```css
/* ─────────────────────────────────────────
   11. 相关文章 / 所属项目
───────────────────────────────────────── */

.related-posts {
  margin-top   : var(--space-xl);
  padding-top  : var(--space-lg);
  border-top   : 1px solid var(--color-border);
}

.related-title {
  font-size     : 0.75rem;
  font-weight   : 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color         : var(--color-text-light);
  margin-bottom : var(--space-md);
}

.post-project {
  font-size    : 0.8rem;
  color        : var(--color-accent);
  background   : var(--color-accent-light);
  padding      : 2px 10px;
  border-radius: 20px;
}

.post-project:hover {
  background: #dde3ff;
}
```

------

### 第六步：给文章加 `project` 字段

打开你想关联的文章，比如：

bash

```bash
nano content/posts/2026-06-03-build-py解析.md
```

在头部加一行：

markdown

```markdown
title: build.py 解析
date: 2026-06-03
tags: 技术
project: 静态博客项目
```

`project` 的值要和 `content/works/` 里对应作品的 `title` 完全一致。

------

全部改完后构建推送：

bash

```bash
python build.py
git add .
git commit -m "add project-post relation"
git push
```

如果没有默认放在基本项目

19:35

打开 `build.py`：

bash

```bash
nano build.py
```

找到 `collect_all_posts` 函数里这行：

python

```python
"project" : meta.get("project", "").strip(),
```

改成：

python

```python
"project" : meta.get("project", "基本项目").strip(),
```

然后在 `content/works/` 下新建一个对应的作品：

bash

```bash
cat > content/works/basic.md
```

markdown

```markdown
title: 基本项目
desc: 未归类的文章都在这里

这里收录了所有未归类的文章。
```

`Ctrl + D` 保存，构建推送：

bash

```bash
python build.py
git add .
git commit -m "add default project"
git push
```

这样所有没有填 `project` 字段的文章，都会自动归到"基本项目"下面。

怎么加projiect

19:43

在文章的头部加一行 `project:` 就行，比如：

bash

```bash
nano content/posts/2026-06-03-build-py解析.md
```

在头部加：

markdown

```markdown
title: build.py 解析
date: 2026-06-03
tags: 技术
project: 静态博客项目
```

`project:` 的值必须和 `content/works/` 里对应作品的 `title` **完全一致**，否则匹配不上。

------

批量加的话，用 `nano` 逐个打开改，或者用 `sed` 一次性加：

bash

```bash
# 给某篇文章加 project 字段（在 tags 那行后面插入）
sed -i '/^tags:/a project: 静态博客项目' content/posts/2026-06-03-build-py解析.md
```

改完后：

bash

```bash
python build.py
git add .
git commit -m "add project fields"
git push
```

