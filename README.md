# IronLog

**本地优先的极简健身追踪器 + AI 教练。** 一个 HTML 文件就是完整应用，零依赖、零后端、离线可用；另附两个可直接侧载安装的 Android APK。

> **在线体验**：部署 GitHub Pages 后访问 `https://yukoooooo.github.io/IronLog/`
> 把 `yukoooooo` / `IronLog` 换成自己的用户名和仓库名即可；用 `publish.py` 推送时会自动替换。
> [下载页](./download.html) 会自动识别 Pages 地址，无需手改任何链接。

| 我想要 | 去哪里 |
| --- | --- |
| 立即在线使用 | [https://yukoooooo.github.io/IronLog/](https://yukoooooo.github.io/IronLog/) |
| 下载 Android 安装包 | [下载页](https://yukoooooo.github.io/IronLog/download.html) 或 [Releases](https://github.com/yukoooooo/IronLog/releases) |
| 看源码 / 自己构建 | 本仓库 `android/`、`native/` 目录 |

| 入口 | 适合场景 | 需要什么 |
| --- | --- | --- |
| [在线网页版](https://yukoooooo.github.io/IronLog/) | 电脑/手机浏览器，或用「添加到主屏幕」装成 PWA | 现代浏览器，无需安装 |
| [Android 下载页](https://yukoooooo.github.io/IronLog/download.html) | 想要原生体验、桌面快捷方式、后台通知 | Android 7.0+，允许「未知来源」 |
| [独立单文件](./IronLog-完整版.html) | 存档、离线双击、发给朋友 | 只需一个浏览器 |

> 上面几个 `YOUR_...` 占位符在 `publish.py` 推送后会自动替换成真实地址。若手动部署，全局替换一次即可。
> 仓库文件导航：[index.html](./index.html) · [download.html](./download.html) · [发布指南](./PUBLISH.md) · [LICENSE](./LICENSE)

---

## 功能

**训练记录**
- 游标轮换分化：推/拉/腿（PPL）、Bro Split、上下肢、全身、自定义
- 84 个动作库，按已勾选器械智能联动；「全部动作库」可添加任意器械动作
- 幽灵值对照上次成绩 + 单手步进器打卡，3 秒完成一组
- 组间休息大号环形倒计时，支持 +30 / -15 / 跳过
- 每个锻炼项目可折叠，历史记录可单日删除

**训练模板**
- 把任意一次训练安排保存为模板（只存动作/组数/目标重量，不存打卡状态）
- 一键套用到今天，或指定日期导入生成同样的训练安排
- 模板列表可查看、删除；随 JSON 备份一起导出导入

**分析与 AI**
- AI 分析范围可选近 7 / 14 / 30 天、**单次训练**或**指定时间段**
- 复盘聚焦当前训练部位，简明输出「建议」+「未来规划」两段
- 无 API Key 时由内置本地智能引擎工作，完全离线
- 可接 DeepSeek / 任意 OpenAI 兼容接口生成结构化训练处方

**可视化与数据**
- 线条勾勒的正面/背面肌肉热力图（按所选范围统计刺激组数）
- 13 周训练日历、容量趋势、四宫格统计
- JSON / CSV 导出，支持 Hevy、Strong 字段映射导入
- API Key 经 WebCrypto AES-GCM 加密后存本地（APK 版用 Android Keystore）

**手机浏览器 App 化**（v1.3）
- 顶部栏真正吸顶、底部导航固定，适配刘海屏与手势条安全区
- 按钮/步进器按原生 APP 触控标准放大（有效热区 ≥40px），输入框统一 16px 避免 iOS 聚焦缩放
- 组行改弹性列，320px 窄屏也不横向溢出
- 内容区**左右滑动切换分页**、弹层顶部**下拉关闭**、点击带轻微触感反馈

---

## 快速开始

### 网页版 / PWA（最简单）

```bash
# 方式一：直接双击 index.html

# 方式二：本地静态服务器（推荐，可启用 PWA 安装与离线缓存）
python -m http.server 8080
# 浏览器打开 http://localhost:8080
```

在 HTTPS 环境（如 GitHub Pages）下，浏览器菜单选择「添加到主屏幕 / 安装应用」即可获得全屏 PWA，之后断网也能用。

手机上的操作与 APP 基本一致：底部四个分页可点击，也可在内容区**左右滑动**切换；弹层从底部升起，按住顶部横条**下拉即可关闭**；每组用 `− / +` 调整重量和次数，右侧 `✓` 打卡后弹出大号休息倒计时。

### Android

从 [下载页](https://yukoooooo.github.io/IronLog/download.html) 或 [Releases](https://github.com/yukoooooo/IronLog/releases) 获取 APK，安装时允许「未知来源」。两个版本可共存对比：

| APK | 包名 | 特点 |
| --- | --- | --- |
| `IronLog-Native-v1.0.0.apk` | `com.ironlog.nativeapp` | 100% 原生 Java 界面，无 WebView，Canvas 自绘图表，体积更小 |
| `IronLog-v1.0.0.apk` | `com.ironlog.app` | WebView 壳，与网页版共用同一份 `index.html`，具备原生 HTTP 桥（AI 接口不受 CORS 限制）、SAF 导入导出 |

> 文件名沿用 v1.0.0，网页版与 WebView APK 内部版本已是 **v1.3.0**（原生 Java 版仍为 v1.2.0-native，本次未改动）。两个 APK 使用同一签名证书，可覆盖升级。

---

## 部署到 GitHub Pages

仓库已内置 `.github/workflows/pages.yml`。推送到 `main` 后自动构建并发布站点：

1. 把本仓库推送到 GitHub
2. 打开 **Settings → Pages → Build and deployment**，Source 选 **GitHub Actions**
3. 等待 Actions 完成，访问 `https://<用户名>.github.io/<仓库名>/`

站点内容包含网页版、PWA 资源、[下载页](https://yukoooooo.github.io/IronLog/download.html) 和两个 APK，因此访客可以直接在线使用，也可以直接点击下载安装。

**发布 Release（可选）**：打一个 `v*` 标签即可自动创建 Release 并附上两个 APK：

```bash
git tag v1.2.0
git push origin v1.2.0
```

详见 `.github/workflows/release.yml`。

---

## 数据与隐私

- **所有训练数据只存在本机**。网页版用 `localStorage` / `IndexedDB`，原生版用 `SharedPreferences`。
- **各端数据相互独立**：浏览器按域名隔离存储，两个 APK 各有自己的沙箱。跨端迁移请用「设置 → 导出 JSON」再在另一端导入。
- **不上传任何数据到服务器**。唯一的网络请求是你主动配置的 AI 接口。
- **API Key 不明文存储**：网页版 WebCrypto AES-GCM（不可导出密钥存 IndexedDB），APK 版 Android Keystore。

### 关于浏览器里的 AI 联网

浏览器直连第三方 API 可能被 **CORS 拦截**。若提示「网络/CORS 拦截」，可以：

- 留空 API Key，使用内置本地智能引擎（无需联网，功能完整）；
- 填一个支持 CORS 的中转地址，或本地 Ollama / LM Studio 接口；
- 改用任一 Android APK —— 原生层发 HTTP 请求，不受同源策略限制。

---

## 自行构建 APK

前置：JDK 11+、Android SDK（含 `build-tools;35.0.0` 与 `platforms;android-34`），并把 `java`/`javac`/`keytool`/`aapt2` 加入 PATH。

```bash
cd android && python build_apk.py     # WebView 版 → IronLog-v1.0.0.apk
cd native  && python build_apk.py     # 100% 原生版 → IronLog-Native-v1.0.0.apk
```

Windows 也可双击各目录下的 `build-apk.bat`。构建脚本会自动把工程镜像到纯英文临时目录（规避 `aapt2` 无法处理中文路径的问题），并在缺少密钥时生成 `keystore/ironlog.jks`。

> **签名密钥请勿提交到公开仓库**（已在 `.gitignore` 排除）。Clone 后自行构建的 APK 与仓库内预置 APK 签名不同，无法覆盖安装；若需继续升级预置版本，请妥善保管原 `keystore/ironlog.jks`。

---

## 目录结构

```
.
├── index.html                  网页版主程序（单文件，含全部 JS/CSS）
├── IronLog-完整版.html          同一份文件的中文名副本，便于存档分发
├── download.html               下载落地页（在线版入口 + 两个 APK）
├── manifest.webmanifest        PWA 清单
├── sw.js                       离线缓存 Service Worker
├── icons/                      PWA 图标
├── IronLog-v1.0.0.apk          WebView 版安装包
├── IronLog-Native-v1.0.0.apk   100% 原生版安装包
├── android/                    WebView 壳源码（Java + 构建脚本）
├── native/                     原生 Java 界面源码（12 个 .java + 构建脚本）
└── .github/workflows/          Pages 与 Release 自动发布
```

技术栈：原生 JavaScript（无框架、无构建步骤）、纯 Android framework Java（无 Gradle / AndroidX / 第三方库）。

---

## 版本

**v1.3.0** — 网页版全面适配手机浏览器：吸顶导航、安全区、大触控目标、弹性组行、滑动切页、下拉关闭弹层，排版与操作贴近原生 APP。

**v1.2.0** — 训练模板、聚焦当前部位的简明 AI 建议与未来规划。此前版本已包含全部动作库、AI 分析范围、醒目休息提醒、项目折叠、单日删除、线条肌肉热力图。

## 许可证

[MIT](./LICENSE)
