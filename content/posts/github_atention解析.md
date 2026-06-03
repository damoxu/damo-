# 搜索功能解析：纯前端搜索

> 不需要后端，不需要数据库，全部在浏览器里完成。

---

## 原理

```
构建时
  build.py 扫描所有文章和作品
      ↓
  生成 search-index.json
  （包含每篇文章的标题、正文、标签、链接）

用户搜索时
  浏览器加载 search-index.json
      ↓
  用 JavaScript 过滤匹配的条目
      ↓
  实时显示结果，高亮关键词
```

---

## search-index.json 结构

```json
[
  {
    "title": "我的第一篇文章",
    "date": "2024-01-01",
    "tags": ["随笔", "开始"],
    "url": "/posts/2024-01-hello-world.html",
    "body": "这是正文的前500个字...",
    "type": "post"
  },
  {
    "title": "我的第一个作品",
    "desc": "一个静态博客生成器",
    "url": "/works/project-one.html",
    "body": "作品详细介绍...",
    "type": "work"
  }
]
```

---

## JavaScript 搜索逻辑

```javascript
// 第一步：加载索引文件
fetch("/damo-/search-index.json")
  .then(response => response.json())
  .then(data => { searchIndex = data; });

// 第二步：过滤匹配项
function doSearch(query) {
  const keyword = query.toLowerCase();
  const matched = searchIndex.filter(item => {
    const inTitle = item.title.toLowerCase().includes(keyword);
    const inBody  = item.body.toLowerCase().includes(keyword);
    const inTags  = (item.tags || []).join(" ").toLowerCase().includes(keyword);
    return inTitle || inBody || inTags;
  });
  renderResults(matched, query);
}

// 第三步：高亮关键词
function highlight(text, query) {
  const regex = new RegExp(`(${query})`, "gi");
  return text.replace(regex, "<mark>$1</mark>");
}
```

---

## 优缺点

**优点：**
- 零后端，纯静态，可以部署到任何地方
- 响应速度极快，本地过滤无网络延迟
- 实现简单，代码易读

**缺点：**
- 文章很多时，search-index.json 体积会变大
- 不支持模糊搜索（输入"博客"不会匹配"部落格"）
- 不支持搜索排序（按相关度排序）

对于个人博客来说，以上缺点完全可以接受。