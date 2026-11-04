# 首次上线（GitHub Pages）

账号：**zhenngbolun**（注意双 n，`zhengbolun` 是另一个人的号）
目标地址：**https://zhenngbolun.github.io**

本地已全部就绪，剩下三件事，其中两件是网页点选，最后一件推给我做也行：

```
给仓库改名  →  加 SSH 公钥  →  push
```

---

## 当前状态

| 项 | 状态 |
|---|---|
| 本地仓库 | 已初始化，分支 `main`，两次提交 |
| 提交内容 | 13 个文件，约 380 KB |
| 提交身份 | `Bolun Zheng <bolunzheng@hdu.edu.cn>`（仓库级，未改全局配置） |
| 远端 origin | 已配置为 `git@github.com:zhenngbolun/zhenngbolun.github.io.git` |
| SSH 密钥 | 已生成 `~/.ssh/id_ed25519`（ed25519，无口令），官方 host key 已预置 |
| Git 版本 | 2.55.0 |
| GitHub 网络 | 直连通畅（0.3s），SSH 22 与 443 均通 |
| 资源路径 | 全部相对路径，根域名 / 子目录都不会 404 |

**注意一个已发现的问题**：你此前建的仓库叫 `.github.io`（缺用户名前缀），它是空的、刚建的，需要改名。见第 1 步。

---

## 第 1 步：把仓库改名

打开 https://github.com/zhenngbolun/.github.io/settings

在页面**最上方** Rename 区域的输入框里，把

```
.github.io
```

改成

```
zhenngbolun.github.io
```

点 **Rename**。

> **为什么**：GitHub 只有把仓库命名为 `<用户名>.github.io` 时才映射到根域名。现在这个 `.github.io` 会被当成普通项目站，访问地址会变成 `https://zhenngbolun.github.io/.github.io/`，多一层且难看。仓库是空的，改名零成本，GitHub 会自动重定向旧地址。

同时确认两项：
- 仓库是 **Public**
- 默认分支是 **main**

---

## 第 2 步：添加 SSH 公钥

打开 https://github.com/settings/ssh/new

| 字段 | 填什么 |
|---|---|
| Title | `Windows 笔记本`（随便起，便于日后辨认） |
| Key type | **Authentication Key** |
| Key | 粘贴下面这整行 |

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAII7ttW4/lspYAjno8WUdDYqj+b2VcyBYnqPb6u6mo9JE bolunzheng@hdu.edu.cn
```

点 **Add SSH key**。

> 公钥可以公开，不敏感 —— 私钥 `id_ed25519` 留在你本机 `~/.ssh/` 里，不需要给任何人。
> 这一步做完，以后所有 push 都免密，不用再管 token。

加完在终端验证一下（Git Bash）：

```bash
ssh -T git@github.com
```

第一次会问 `Are you sure you want to continue connecting?` → 输 `yes`。
看到 `Hi zhenngbolun! You've successfully authenticated` 就通了。**这句里的 `but GitHub does not provide shell access` 是正常提示，不是错误。**

---

## 第 3 步：推送

```bash
cd /c/Users/1/WorkBuddy/Claw/homepage
git push -u origin main
```

成功标志：终端最后出现 `branch 'main' set up to track 'origin/main'`。

刷新 https://github.com/zhenngbolun/zhenngbolun.github.io ，应该能看到 `index.html`、`assets/`、`data/` 等文件。

> 这一步你直接把结果告诉我，我来执行也可以 —— 认证配好后我这边就能直接推。

---

## 第 4 步：开启 Pages

仓库 → **Settings** → 左侧 **Pages**

| 字段 | 选什么 |
|---|---|
| Source | **Deploy from a branch** |
| Branch | **main**，右侧目录保持 **/ (root)** |
| | 点 **Save** |

保存后顶部会出现 "Your site is live at ..."，但**先别急着点**——通常需要 **1–2 分钟**，首次有时 5 分钟。

进度看仓库顶部的 **Actions** 标签页，`pages build and deployment` 变绿即完成。

---

## 第 5 步：验收

地址：**https://zhenngbolun.github.io**

- [ ] 首页正常，导航栏、头像、News 都在
- [ ] 点 **Publications** 能进论文页，93 篇按年份分组
- [ ] 论文标题能点开 DOI
- [ ] 手机打开排版正常（不横向裁切）
- [ ] 地址栏有 BZ 小图标

**第 2 项最容易出问题。** 如果论文页一直 "Loading…"，按 F12 看 Console：

| 报错 | 原因 | 修法 |
|---|---|---|
| `404` 指向 `data/papers.json` | 文件没推上去 | 补推该文件 |
| `CORS` / `Failed to fetch` | 用 `file://` 打开了本地文件 | 换 `https://` 地址访问 |
| 列表空白但无报错 | JSON 语法错 | 用在线校验器查 `papers.json` |

**整站 404**：查 ① 仓库名是否 `zhenngbolun.github.io` ② 是否 Public ③ Pages 分支是否 main / root ④ Actions 是否变绿。

**能开但没样式**：`.nojekyll` 没推。它是空文件，在仓库页面 Add file → Create new file，文件名填 `.nojekyll`，内容留空，提交即可。

---

## 之后的日常更新

本地改完文件，三条命令：

```bash
git add .
git commit -m "更新论文列表"
git push
```

推完等 1–2 分钟自动生效，**不用再碰 Pages 设置**。

---

## 附：不想用 SSH 的备选方案

如果哪天换电脑、不想配密钥，改用 HTTPS + Token：

1. https://github.com/settings/tokens → Generate new token (classic) → 勾 `repo` → 生成后立刻复制 `ghp_...`
2. `git remote set-url origin https://github.com/zhenngbolun/zhenngbolun.github.io.git`
3. push 时 Password 处粘贴 token（不是登录密码）

Token 可以随时在同一个页面 Revoke，比密码安全。

---

## 两个可选增强

### 绑自己的域名

有 `bolunzheng.com` 之类的域名才需要。仓库 Settings → Pages → Custom domain 填域名，去域名商加一条 CNAME 记录，然后勾选 **Enforce HTTPS**。

### 国内访问慢

`github.io` 在国内时通时不通，这是 GitHub 的网络问题，不是网站的问题。三个缓解办法：

1. **什么都不做** —— 主页受众是审稿人、合作者、申请学生，他们的网络基本正常
2. **加国内镜像** —— 同一份代码同时推 Gitee Pages（需实名）
3. **换托管** —— Cloudflare Pages 国内可访问性更好，免费且支持自定义域名

迁移的话代码一行都不用改，只改部署方式。

