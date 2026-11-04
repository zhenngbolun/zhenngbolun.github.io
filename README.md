# Bolun Zheng — academic homepage

纯静态站点，无构建步骤、无外部依赖（字体、图标、脚本全部本地）。
版式参照 [al-folio](https://github.com/alshedivat/al-folio)：顶部导航、930px 正文宽度、
大字号姓名标题、`News` 无边框表格、论文条目左侧 venue 徽章。

改内容 = 改文件，推送 = 上线。

> 具体的「改哪里、怎么改」速查见 **[EDITING.md](EDITING.md)**。

```
homepage/
├── index.html            首页
├── publications.html     完整论文列表（按年份分组 + 筛选）
├── data/
│   └── papers.json       论文数据库，唯一数据源
├── assets/
│   ├── css/style.css     全部样式
│   ├── js/papers.js      渲染论文列表
│   └── img/avatar.svg    头像占位（换成你的照片）
├── build_papers.py       从 OpenAlex 同步论文（可选）
├── .nojekyll             告诉 GitHub Pages 不要跑 Jekyll
└── .gitignore
```

---

## 部署到 GitHub Pages

### 1. 建仓库

| 仓库名 | 网址 | 说明 |
|---|---|---|
| `<用户名>.github.io` | `https://<用户名>.github.io` | **推荐**，根域名 |
| 任意，如 `homepage` | `https://<用户名>.github.io/homepage/` | 路径多一层 |

### 2. 推送

在 `homepage/` 目录下执行：

```bash
git init
git add .
git commit -m "Add academic homepage"
git branch -M main
git remote add origin https://github.com/<用户名>/<仓库名>.git
git push -u origin main
```

> 推的是 `homepage/` **里面的内容**，仓库根目录下应当直接看到 `index.html`。

### 3. 打开 Pages

仓库 → **Settings** → **Pages** → Source 选 **Deploy from a branch** →
Branch **main**，目录 **/ (root)** → Save。等 1–2 分钟即可访问。

---

## 改内容

### 加一篇论文

只改 `data/papers.json`：

```json
{
  "title": "Paper title",
  "authors": ["First Author", "Bolun Zheng", "Last Author"],
  "venue": "IEEE TIP",
  "venue_full": "IEEE Transactions on Image Processing",
  "year": 2027,
  "type": "journal",
  "doi": "10.1109/TIP.2027.xxxxxxx",
  "url": "https://doi.org/10.1109/TIP.2027.xxxxxxx",
  "cites": 0,
  "selected": false
}
```

- `type`：`journal` / `conference` / `preprint`
- `selected: true` → 出现在首页 Selected Publications
- `venue` 是左侧徽章上的短名；`venue_full` 是条目下方斜体全名
- 徽章配色规则写在 `assets/js/papers.js` 的 `TIER1` 数组里：
  该数组中的 venue 显示为深蓝实心，其余灰色描边，`preprint` 显示为橙色
- 本人姓名必须写成 `Bolun Zheng` 才会加粗
- `url` 留空则标题不可点、不显示按钮

### 从 OpenAlex 重新同步

```bash
python build_papers.py
```

首次运行会联网抓取（约 2 MB，存为 `oa_works.json`，已 gitignore），之后复用本地缓存。
换作者只需改脚本顶部的 `AUTHOR_ID`。

**注意**：会覆盖 `data/papers.json`，手工加的条目和手调的 `selected` 会丢失。
日常加论文直接改 JSON 即可，不必跑这个脚本。

### 换头像

把正方形照片（≥400×400）命名为 `avatar.jpg` 放进 `assets/img/`，然后把两个 HTML 里
全部 3 处 `avatar.svg` 改成 `avatar.jpg`（`index.html` 2 处、`publications.html` 1 处）。

---

## 本地预览

`fetch()` 需要 HTTP，双击打开是看不到论文列表的：

```bash
python -m http.server 8788
```

访问 http://localhost:8788

---

## 上线前需要确认

1. **邮箱** `bolunzheng@hdu.edu.cn` —— 出现在 `index.html` 两处
2. **GitHub 用户名** —— 侧栏/页脚尚未加入 GitHub 链接，拿到后补一个 `<a>`
3. **地址** —— 按杭电下沙校区通用地址填写
4. **Teaching** —— 目前只写了 Machine Vision 一门
5. **News 四条** —— 依据论文数据推断，仅到年份级，月份与措辞请按实际改
6. **论文作者列表** —— 来自 OpenAlex，中文拼音姓名偶有错拼，建议抽查
