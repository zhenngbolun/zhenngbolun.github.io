# 上线记录与重建指引（GitHub Pages）

## 状态：已上线

**https://zhenngbolun.github.io**

2026-11-04 15:31 首次部署成功。

账号 `zhenngbolun`（注意双 n，`zhengbolun` 是另一个人的号）。

推送 → 自动构建 → 约 100 秒后生效。整个过程**不需要手动开启 Pages**（见下方说明）。

---

## 已完成的事项

| 项 | 结果 |
|---|---|
| 本地仓库 | 已初始化，分支 `main` |
| 提交内容 | 12 个文件，共 118 KB |
| 提交身份 | `Bolun Zheng <bolunzheng@hdu.edu.cn>`（仓库级，未改全局配置） |
| 远端 origin | `git@github.com:zhenngbolun/zhenngbolun.github.io.git` |
| SSH 认证 | 已配置 ed25519 密钥，`ssh -T git@github.com` 返回 `Hi zhenngbolun!` |
| 仓库可见性 | Public |
| Pages | 首次推送后**自动启用**并部署 |
| 线上验收 | 全部资源 200；93 篇论文 / 14 篇精选 / 全部带 DOI |
| 修复记录 | 预印本链接标签曾一律显示 `arXiv`，SSRN 那条标错，已改为按 venue 判断 |

**过程中踩到的坑**：仓库最初被建成 `.github.io`（缺用户名前缀），已改名为 `zhenngbolun.github.io`。GitHub 只有这种命名才映射到根域名。

---

## 日常更新（最常做的事）

```bash
cd /c/Users/1/WorkBuddy/Claw/homepage
git add .
git commit -m "更新论文列表"
git push
```

推完等 **1–2 分钟**自动重新部署，不需要碰任何设置。

加论文改 `data/papers.json`，改文字改 HTML，改配色改 CSS 变量 —— 详见 [EDITING.md](EDITING.md)。

---

## 页面的开启机制（重要）

**不需要手动去 Settings → Pages 配置。** 当仓库命名为 `<用户名>.github.io` 且首次推送时，GitHub 会自动启用 Pages 并触发 `pages build and deployment`。

如果哪天需要手动确认，检查：
- 仓库 Settings → Pages 中应显示 "Your site is live at https://zhenngbolun.github.io"
- Actions 标签页应有 `pages build and deployment` 且为绿色

**若确实没有自动启用**（极少见），手动配置：
Settings → Pages → Source 选 `Deploy from a branch` → Branch `main` + `/ (root)` → Save。

---

## 从零重建（换机器或误删时）

```bash
# 1. 克隆
git clone git@github.com:zhenngbolun/zhenngbolun.github.io.git
cd zhenngbolun.github.io

# 2. 换机器时需要重新配 SSH（公钥贴到 https://github.com/settings/ssh/new）
ssh-keygen -t ed25519 -C "bolunzheng@hdu.edu.cn"

# 3. 改完推送
git add . && git commit -m "update" && git push
```

---

## 排错

**整站 404**：查 ① 仓库名是否 `zhenngbolun.github.io` ② 是否 Public ③ Actions 是否变绿 ④ 推送后是否不到 1 分钟。

**论文页一直 "Loading…"**：按 F12 看 Console。

| 报错 | 原因 | 修法 |
|---|---|---|
| `404` 指向 `data/papers.json` | 该文件没推上去 | 补推 |
| `CORS` / `Failed to fetch` | 用 `file://` 打开了本地文件 | 换 `https://` 访问 |
| 列表空白无报错 | JSON 语法错 | 在线校验器查 `papers.json` |

**能开但没样式**：`.nojekyll` 没推。仓库页面 Add file → Create new file，文件名 `.nojekyll`，内容留空，提交。

**改了文件线上没变**：① 是否 `git push` 了 ② 等 1–2 分钟 ③ 浏览器 Ctrl+F5 强刷 ④ GitHub 对静态文件有约 10 分钟 CDN 缓存

---

## 已知的"看着像问题但不是问题"

- **标题里 From / With / For 大写**：这是 IEEE 的 Title Case 规范（4 字母以上虚词大写），各期刊原文如此，不是数据错误，**不要统一改小写**
- **SSRN 徽章是浅橙色**：`preprint` 类型统一用橙色调，正常的
- **`zhengbolun` 能打开但只有 1 个仓库**：那是别人的账号，与你无关

---

## 附：SSH 备选方案（HTTPS + Token）

换电脑且不想配密钥时：

1. https://github.com/settings/tokens → Generate new token (classic) → 勾 `repo` → 立刻复制 `ghp_...`
2. `git remote set-url origin https://github.com/zhenngbolun/zhenngbolun.github.io.git`
3. push 时 Password 处粘贴 token（不是登录密码）

---

## 两个可选增强

### 绑自己的域名

有域名才需要。Settings → Pages → Custom domain 填域名，域名商处加 CNAME 记录，勾选 **Enforce HTTPS**。

### 国内访问慢

`github.io` 在国内时通时不通，是 GitHub 的网络问题，不是网站的问题。

1. **什么都不做** —— 主页受众是审稿人、合作者、申请学生，网络基本正常
2. **加国内镜像** —— 同一份代码同时推 Gitee Pages（需实名）
3. **换托管** —— Cloudflare Pages 国内可访问性更好，免费且支持自定义域名

迁移的话代码一行都不用改，只改部署方式。


