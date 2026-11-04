# 首次上线（GitHub Pages）

本地已经准备完了，现在只差远端三步：

```
建仓库  →  传代码  →  开 Pages
```

下面每一步都写了具体点哪里。全程约 5 分钟。

---

## 当前状态

| 项 | 状态 |
|---|---|
| 本地仓库 | 已初始化，分支 `main` |
| 首次提交 | 已完成（`de103a5`，11 个文件） |
| 提交身份 | `Bolun Zheng <bolunzheng@hdu.edu.cn>`（仓库级，未改你的全局配置） |
| Git 版本 | 2.55.0 |
| GitHub 网络 | 直连通畅（0.3s） |
| 资源路径 | 全部相对路径，根域名 / 子目录都不会 404 |

所以现在**不需要**再动代码，只需要建一个仓库把本地推上去。

---

## 第 1 步：建仓库

打开 https://github.com/new

依次填：

| 字段 | 填什么 | 说明 |
|---|---|---|
| Repository name | **`你的用户名.github.io`** | 例：用户名是 `bolunzheng`，就填 `bolunzheng.github.io` |
| Description | 可留空 | |
| Public / Private | **必须选 Public** | Private 用 Pages 需要付费 Pro |
| Add a README file | **不要勾** | ⚠️ 勾了会让 push 失败（远端有文件、本地也有历史） |
| Add .gitignore | **None** | 我们自带 |
| Choose a license | 可留空 | |

点 **Create repository**。

> **为什么名字必须是 `用户名.github.io`**：这是 GitHub 的特殊规则，只有这种命名的仓库才能映射到根域名 `https://用户名.github.io`。用别的名字（如 `homepage`）也能跑，但地址会变成 `https://用户名.github.io/homepage/`，多一层路径，不好看。本站全部用相对路径，两种都能正常工作。

建完你会看到一个空仓库页面，上面有一条 `git remote add origin ...` 命令 —— 复制那个 URL 备用。

---

## 第 2 步：上传代码

### 方式 A：命令行（推荐，以后更新也用它）

在 `homepage/` 目录下执行，**把 `<你的用户名>` 换成实际值**：

```bash
git remote add origin https://github.com/<你的用户名>/<你的用户名>.github.io.git
git push -u origin main
```

**这一步会要求验证身份。** GitHub 自 2021 年起不接受账号密码，必须用 Personal Access Token（PAT）。第一次用需要先申请一个：

1. 打开 https://github.com/settings/tokens
2. 点 **Generate new token** → 选 **Tokens (classic)**
3. Note 随便填，如 `homepage`；Expiration 建议选 **90 days** 或 **No expiration**
4. 勾选权限：**只需勾 `repo`**（第一个大项，勾上后子项会自动全选）
5. 拉到底点 **Generate token**
6. **立刻复制那串 `ghp_...`** —— 页面关掉就再也看不到了，只能重新生成

回到终端执行 push：

- 弹出的窗口如果要求 **Username** → 填 GitHub 用户名
- 要求 **Password** → **粘贴那个 `ghp_...` token**（不是你的登录密码）

> 想避免每次输 token，可以打开 Windows「凭据管理器」→ Windows 凭据 → 找到 `git:https://github.com` → 编辑，把用户名改成 token。之后再 push 就不会再问。

**push 成功的标志**：终端最后出现 `branch 'main' set up to track 'origin/main'`。刷新 GitHub 页面，文件已经在了。

### 方式 B：网页拖拽（不想碰命令行时）

1. 在空仓库页面点 **uploading an existing file**
2. 打开 `C:\Users\1\WorkBuddy\Claw\homepage\`，**框选里面的全部内容**（`index.html`、`assets`、`data` 等）拖进浏览器
   - ⚠️ 拖的是文件夹**里面的东西**，不要拖 `homepage` 文件夹本身，否则会变成 `homepage/index.html`，首页打不开
   - `.nojekyll` 和 `.gitignore` 是隐藏文件，拖拽可能漏掉。`.nojekyll` 建议手动建一个空文件补上
3. 底部 Commit changes

---

## 第 3 步：开启 Pages

仓库 → **Settings**（顶部菜单）→ 左侧 **Pages**

| 字段 | 选什么 |
|---|---|
| Source | **Deploy from a branch** |
| Branch | **main**，右边目录保持 **/ (root)** |
| | 点 **Save** |

保存后页面顶部会出现一行 "Your site is live at ..."，但**先别急着点**——GitHub 需要构建，通常 **1–2 分钟**，首次有时 5 分钟。

进度可以在这里看：仓库顶部 **Actions** 标签页，会有一个 `pages build and deployment` 在跑，变绿就完成了。

---

## 第 4 步：验收

地址：`https://<你的用户名>.github.io`

按这五项逐个确认：

- [ ] 首页正常显示，导航栏、头像、News 都在
- [ ] 点 **Publications** 能进论文页，93 篇按年份分组列出
- [ ] 论文条目的标题能点开 DOI
- [ ] 手机浏览器打开排版正常（导航不挤、不横向裁切）
- [ ] 地址栏有小图标（头像那个 BZ）

**第 2 项最容易出问题**。如果论文页显示 "Loading…" 一直不动，或者首页 Selected Publications 空白，按 F12 打开 Console 看报错：

| 报错 | 原因 | 修法 |
|---|---|---|
| `404 (Not Found)` 指向 `data/papers.json` | 文件没传上去 | 补传 `data/papers.json` |
| `CORS` / `Failed to fetch` | 用 `file://` 直接打开了本地文件 | 换成 `https://` 地址访问 |
| 什么都没有但列表空白 | JSON 语法错 | 用在线 JSON 校验器查 `papers.json` |

**整站 404**：依次查 ① 仓库名拼写 ② 是否 Public ③ Pages 里分支是否 main / root ④ 是否还在构建（看 Actions 有没有变绿）。

**页面能开但没样式**：`.nojekyll` 没传。它是空文件，在仓库页面点 Add file → Create new file，文件名填 `.nojekyll`，内容留空，提交即可。

---

## 之后的日常更新

本地改完文件，三条命令：

```bash
git add .
git commit -m "更新论文列表"
git push
```

推完等 1–2 分钟自动生效，**不用再去动 Pages 设置**。

---

## 两个可选增强

### 绑自己的域名

有 `bolunzheng.com` 之类的域名才需要这步。仓库 Settings → Pages → Custom domain 填域名，然后去域名商那里按 GitHub 给的提示加一条 CNAME 记录。开启 **Enforce HTTPS** 勾选即可。

### 国内访问慢的问题

`github.io` 在国内访问时好时坏，这是 GitHub 本身的网络问题，不是网站的问题。三个缓解办法，按推荐程度：

1. **什么都不做** —— 主页的主要受众是审稿人、合作者、申请学生，海外和机构的网络基本都正常
2. **加一个国内镜像** —— 同一份代码可以同时推到 Gitee Pages（需要实名），两个地址并存
3. **换托管** —— Cloudflare Pages 在国内可访问性更好，且免费、支持自定义域名

如果决定要做镜像或迁移，跟我说，代码不用改，改的是部署方式。
