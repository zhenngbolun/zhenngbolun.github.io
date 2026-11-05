# 改站手册

三种改动，三个文件，互不干扰：

| 你想改的东西 | 打开 | 怎么定位 |
|---|---|---|
| 页面上的文字、板块 | `index.html` / `publications.html` | Ctrl+F 搜你在页面上看到的那句话 |
| 颜色、字号、宽度、间距 | `assets/css/style.css` | 只改文件顶部 `:root` 里的变量 |
| 论文条目 | `data/papers.json` | 直接加/删一段 JSON |

改完 **保存 → 浏览器刷新** 就能看到效果。预览服务器已经在 `http://localhost:8788` 跑着。

---

## 一、页面文字

`index.html` 里每个板块前面都有一行注释，直接搜注释就能跳过去：

| 搜这行 | 到的板块 |
|---|---|
| `<!-- ======================= about` | 个人简介、Email、地址 |
| `<!-- ======================= news` | News |
| `<!-- ======================= openings` | Openings（招生） |
| `<!-- ======================= publications` | 精选论文（自动生成，别在这里加论文） |
| `<!-- ======================= teaching` | 授课 |
| `<!-- ======================= contact` | 联系、Scholar/DBLP 链接 |

### 改姓名标题

搜 `<h1><strong>Bolun</strong> Zheng</h1>`

前面粗体、后面细体。想全都粗就把整个名字放进 `<strong>`；想换顺序、加中文名都在这一行。

### 改头衔

搜 `Associate Professor, School of Automation`

那行的 `<span class="sep">·</span>` 是中间的圆点，**前后都别删**，否则两段会粘一起。

### 加一条 News

搜 `Nov 2026`，在它上面插一段，格式照抄：

```html
      <tr>
        <th scope="row">Dec 2026</th>
        <td>一句话，可以用 <strong>加粗</strong> 强调期刊名。</td>
      </tr>
```

News 是**从上往下**排的，新的放最上面。

### 删掉整个板块

比如不想放 Openings：删掉从 `<!-- ======================= openings` 到紧跟的 `</section>` 之间的全部内容。

⚠️ 导航栏里对应的 `<li><a href="#openings">…</a></li>` 也要一起删，否则点了没反应。导航在文件靠上的 `<ul class="nav-links">` 里。

### 加一个新板块

在任意两个 `</section>` 之间插：

```html
  <!-- ======================= talks ======================= -->
  <section id="talks">
    <h2>Talks</h2>
    <p>正文。</p>
  </section>
```

然后到导航 `<ul class="nav-links">` 里加 `<li><a href="#talks">Talks</a></li>`。样式会自动生效，不用碰 CSS。

---

## 二、颜色与尺寸

`assets/css/style.css` 第 7–25 行是 `:root`，**整站的颜色和尺度都在这里**，改一处全站生效：

```css
--brand:      #00369f;   /* 主色：选中项下划线、链接、顶刊徽章 */
--measure:    930px;     /* 正文最大宽度，改小则两侧留白更多 */
--nav-h:      58px;      /* 顶部导航高度 */
--ink:        #111214;   /* 主文字色 */
--ink-2:      #4a4f57;   /* 次级文字 */
```

### 常见调整

| 想要 | 改法 |
|---|---|
| 换主色（比如改成深红） | `--brand: #8b1a1a;` 和 `--brand-dk: #6b1212;` |
| 全站字大一点 | `body { font-size: 16px }` → `17px`（搜 `font-size: 16px`） |
| 正文更窄更集中 | `--measure: 930px` → `820px` |
| 姓名标题更大 | 搜 `.page-head h1`，改 `font-size` |
| 行距松一点 | `body { line-height: 1.68 }` → `1.75` |

**不建议**逐条改各处的 px 值——那会把整体的比例关系打散。要调就调变量。

---

## 三、论文列表

**唯一的数据库是 `data/papers.json`**，首页的 Selected 和 Publications 页都从它读。

### 加一篇

在数组里任意位置插一段（顺序无所谓，页面会自己按年份排）：

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
  "selected": false,
  "rank": 0,
  "project": ""
}
```

六个容易踩的点：

1. **`"Bolun Zheng"` 必须一字不差**，才会加粗显示你的名字。中文拼音顺序要以出版版本为准。
2. **`selected: true`** 才会出现在首页。目前正好 14 篇。
3. **`rank`** 决定首页顺序，`1` 是最上面那篇，依次往后。**新增精选时把 rank 填成合适的序号，并把后面各篇的 rank 顺延**，否则会出现并列或空号（并列时按年份倒序兜底）。
4. **`project`** 填开源代码或项目主页链接（如 GitHub）。填了就会在 DOI 右边多出一个 `Project` 按钮；留空 `""` 就不显示。
5. **`venue` 是徽章短名**，要和 `assets/js/papers.js` 里的 `TIER1` 数组写法一致才能拿到深蓝实心样式。不在里面的会自动变灰框。
6. **逗号**：JSON 不允许最后一项后面有逗号。加完如果不显示，先检查这个。

> 顺序只影响首页。Publications 页按年份自动分组，不看 rank。

改完刷新页面就能看到，**不需要跑任何脚本**。

### 删一篇 / 换精选

直接删掉对应的 `{ … }` 整段；换精选只改 `"selected": false` ↔ `true`。

### 重新排序

不需要。`papers.js` 会按 `year` 倒序、同年按 `cites` 排。

### 什么时候才需要跑脚本

```bash
python build_papers.py
```

只有**想让 OpenAlex 重新抓一遍**时才用。注意它会**覆盖 `papers.json`**，手工加的条目和你调过的 `selected`／`rank`／`project` 全部按 `build_papers.py` 里的 `SELECTED` 和 `PROJECTS` 重算，手改的值会丢。日常加论文请直接改 JSON。

---

## 四、换头像

1. 正方形照片（≥400×400）命名为 `avatar.jpg`，放进 `assets/img/`
2. 两个 HTML 文件里搜 `avatar.svg` 全改成 `avatar.jpg`，**共 3 处**：
   - `index.html` 两处（第 10 行浏览器标签图标、第 64 行页面头像）
   - `publications.html` 一处（第 9 行标签图标）

照片会自动裁成圆形，取的是中心区域，构图请把人脸放中间偏上。

---

## 五、预览与上线

### 本地看

服务器已经在跑：**http://localhost:8788**

如果哪天关了，在 `homepage/` 目录下重启：

```bash
python -m http.server 8788
```

> 必须用 `http://` 打开，`fetch()` 读 JSON 受浏览器安全策略限制，**双击文件是看不到论文列表的**。

### 上线

```bash
git add .
git commit -m "update"
git push
```

推完等 1–2 分钟，GitHub Pages 自动重新部署。首次部署的完整步骤见 `README.md`。

---

## 六、改坏了怎么办

所有文件都是纯文本，没有编译过程，**改坏了一定能退回**：

```bash
git checkout -- index.html          # 撤销单个文件
git checkout -- .                   # 撤销全部未提交的修改
```

没初始化 git 之前，最稳的办法是动手前先复制一份 `index.html` 备份。

---

## 七、你随时可以让我改

这些都是一句话的事，不用自己动手：

- 加板块（Talks / Awards / Students / Service / 专利列表）
- 中英双语切换
- 首页论文配缩略图
- 加访问统计、加暗色模式
- 整体换一套版式

说清楚要什么效果就行，改完我照样截图自查一遍再给你看。
