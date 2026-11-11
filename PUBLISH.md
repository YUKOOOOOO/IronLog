# 发布到 GitHub · 操作指南

当前环境没有配置 GitHub 凭据（未安装 `gh`、无 token），因此仓库已经**准备到「只差最后一步推送」**的状态：
文件齐全、`.gitignore` 已排除签名密钥、Git 仓库已初始化并完成首次提交。

选一种方式完成推送即可。

---

## 方式 A：一键脚本（推荐）

```bash
python publish.py
```

脚本会依次：

1. 发布前自检（必需文件、签名密钥是否被排除、git / gh 是否可用）
2. 确保 Git 提交身份（只写**仓库级**配置，不污染全局）
3. `git add -A` + 首次提交（自动拒绝任何密钥文件进入暂存区）
4. 询问 GitHub 用户名与仓库名
5. 优先用已登录的 `gh` 自动建仓并推送；否则引导用网页建空仓库后 `git push`
6. 推送成功后自动把 README 中的 `YOUR_USERNAME` / `YOUR_REPO` 换成真实地址并再提交一次

只想自检、不推送：`python publish.py --check`

---

## 方式 B：手动命令

```bash
git remote add origin https://github.com/你的用户名/ironlog.git
git branch -M main
git push -u origin main
```

GitHub 已不支持账号密码推送，需要 Personal Access Token 或已登录的凭据管理器。
更省事的是装 [GitHub CLI](https://cli.github.com/) 后：

```bash
gh auth login
gh repo create ironlog --public --source=. --remote=origin --push
```

---

## 方式 C：完全不用命令行（网页拖拽上传）

1. 打开 <https://github.com/new>，仓库名填 `ironlog`，选 **Public**，**不要**勾选 README / .gitignore / License
2. 创建后点 「uploading an existing file」，把本目录文件拖进去
   - **务必不要上传** `android/keystore/` 和 `native/keystore/` 里的 `.jks` 文件
   - 保留 `.github/`、`icons/` 等目录结构
3. 提交后照下方步骤开启 Pages
4. 此方式下 README 里的 `YOUR_USERNAME` / `YOUR_REPO` 需要手动全局替换一次

---

## 推送后：开启在线版（关键两步）

**1. 开启 Pages**

打开 `https://github.com/<用户名>/ironlog/settings/pages` →
**Build and deployment → Source** 选 **GitHub Actions**。

`.github/workflows/pages.yml` 会自动组装站点并发布，只上传：
`index.html`、`download.html`、`IronLog-完整版.html`、`manifest.webmanifest`、`sw.js`、
`icons/`、两个 APK、`README.md`、`LICENSE` 与 `.nojekyll` —— **不含任何 Java 源码或密钥**。

完成后访问：

```
https://<用户名>.github.io/ironlog/            在线使用
https://<用户名>.github.io/ironlog/download.html   下载 Android 版
```

下载页会自动识别 Pages 地址，生成正确的仓库 / Releases 链接，不需要改代码。

**2. 发布 Release（可选）**

```bash
git tag v1.2.0
git push origin v1.2.0
```

`.github/workflows/release.yml` 会自动创建 Release 并附上两个 APK 与独立 HTML 版。
也可在 Actions 页面手动运行 `Publish Release (APK)` 并填标签。

---

## 安全清单

- `android/keystore/ironlog.jks`、`native/keystore/ironlog.jks` 是签名私钥，**永远不要提交**
  （已在 `.gitignore` 排除，`publish.py` 也会二次拦截）
- 从 GitHub 克隆后自行构建出的 APK 与仓库内预置 APK 签名不同，无法覆盖安装；
  如需继续升级已发布的 APK，请自行妥善保管原 keystore
- 构建脚本里的 `ironlog2026` 是开发用演示口令，仅用于本地生成调试密钥，与线上数据无关
- 训练数据、API Key 都只存在使用者本机，仓库里没有任何真实用户数据

---

## 已知限制（已在文档如实说明）

- 浏览器直连第三方 AI 接口可能被 **CORS** 拦截；留空 API Key 即可用内置本地智能引擎（完全离线）
- 网页版按域名隔离存储，两个 APK 各有沙箱，**各端数据不互通**，跨端用 JSON 导出/导入
- GitHub Pages 是静态托管，不提供后端，也不收集任何数据
