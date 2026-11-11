# -*- coding: utf-8 -*-
"""
IronLog 一键发布助手

把当前目录初始化为 Git 仓库、做首次提交，并推送到 GitHub。
优先使用已登录的 GitHub CLI（gh）；没有 gh 时则引导用网页创建空仓库后推送。

用法：
    python publish.py                 # 交互式
    python publish.py --check         # 只做发布前自检，不推送
"""
import os
import sys
import shutil
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))


def run(args, cwd=HERE, check=False, capture=False):
    try:
        r = subprocess.run(
            args, cwd=cwd, check=check,
            capture_output=capture, text=True,
            encoding="utf-8", errors="replace",
        )
        return r
    except FileNotFoundError:
        return None
    except subprocess.CalledProcessError as e:
        print("  命令失败：", " ".join(args))
        print("  ", (e.stderr or e.stdout or "").strip()[:500])
        return e


def out(args, cwd=HERE):
    r = run(args, cwd=cwd, capture=True)
    return (r.stdout or "").strip() if r and hasattr(r, "stdout") else ""


def say(msg):
    print(msg, flush=True)


def precheck():
    say("\n=== 发布前自检 ===")
    ok = True

    required = [
        "index.html", "IronLog-完整版.html", "download.html",
        "manifest.webmanifest", "sw.js", "README.md", "PUBLISH.md", "LICENSE",
        ".gitignore", ".nojekyll", "publish.py",
        "icons/icon-192.png", "icons/icon-512.png",
        "IronLog-v1.0.0.apk", "IronLog-Native-v1.0.0.apk",
        ".github/workflows/pages.yml", ".github/workflows/release.yml",
    ]
    for f in required:
        p = os.path.join(HERE, f)
        good = os.path.isfile(p)
        if not good:
            ok = False
        say("  %s %s" % ("OK  " if good else "MISS", f))

    # 密钥绝不能进仓库
    leaks = []
    for root, dirs, files in os.walk(HERE):
        if ".git" in root.split(os.sep):
            continue
        for n in files:
            if n.endswith((".jks", ".keystore", ".pepk", ".p12")):
                leaks.append(os.path.relpath(os.path.join(root, n), HERE))
    if leaks:
        r = out(["git", "check-ignore"] + leaks)
        ignored = [x for x in r.splitlines() if x.strip()]
        say("  INFO 本机有 %d 个签名密钥（属正常，仅用于本地构建）：" % len(leaks))
        for p in leaks:
            say("       " + p)
        say("  %s 已被 .gitignore 排除：%d / %d" %
            ("OK  " if len(ignored) == len(leaks) else "FAIL", len(ignored), len(leaks)))
        if len(ignored) != len(leaks):
            ok = False
            say("       !! 有密钥未被排除，请检查 .gitignore")
    else:
        say("  OK   本机无密钥文件（克隆后首次构建会自动生成）")

    say("  git: %s" % (shutil.which("git") or "未找到"))
    say("  gh : %s" % (shutil.which("gh") or "未安装（可选）"))
    say("  自检结果：%s" % ("通过" if ok else "存在问题，请先修复"))
    return ok


def ensure_identity():
    name = out(["git", "config", "user.name"])
    email = out(["git", "config", "user.email"])
    if name and email:
        say("  Git 身份：%s <%s>" % (name, email))
        return True
    say("\n本机尚未配置 Git 提交身份。")
    name = input("  你的名字（直接回车用 IronLog）：").strip() or "IronLog"
    email = input("  你的邮箱（直接回车用 ironlog@users.noreply.github.com）：").strip() \
        or "ironlog@users.noreply.github.com"
    # 只写仓库级配置，不污染全局
    run(["git", "config", "user.name", name])
    run(["git", "config", "user.email", email])
    say("  已设置仓库级身份：%s <%s>" % (name, email))
    return True


def init_and_commit():
    if not os.path.isdir(os.path.join(HERE, ".git")):
        say("\n=== 初始化 Git 仓库 ===")
        r = run(["git", "init", "-b", "main"], capture=True)
        say("  git init: %s" % ("完成" if r and r.returncode == 0 else "失败"))
    else:
        say("\n=== 已有 Git 仓库 ===")

    ensure_identity()
    say("\n=== 暂存文件 ===")
    r = run(["git", "add", "-A"], capture=True)
    if r is None or r.returncode != 0:
        say("  git add 失败")
        return False
    staged = out(["git", "diff", "--cached", "--name-only"])
    lines = [x for x in staged.splitlines() if x.strip()]
    say("  待提交 %d 个文件" % len(lines))
    # 安全检查：任何密钥文件都不允许进入暂存区
    bad = [x for x in lines if x.lower().endswith((".jks", ".keystore", ".pepk", ".p12"))]
    if bad:
        say("  !! 暂存区含密钥文件，已停止：" + ", ".join(bad))
        return False
    apk = [x for x in lines if x.endswith(".apk")]
    say("  其中安装包：%s" % (", ".join(apk) if apk else "（无变化）"))

    status = out(["git", "status", "--porcelain"])
    if not status:
        say("  没有需要提交的改动，跳过提交。")
        return True
    r = run(["git", "commit", "-m", "IronLog v1.2.0: 训练模板 + 聚焦当前部位的简明 AI 分析"], capture=True)
    if r and r.returncode == 0:
        say("  首次提交完成")
        return True
    say("  git commit 未成功：%s" % ((r.stdout or "") + (r.stderr or "") if r else ""))
    return False


def push_with_gh(user, repo):
    say("\n=== 使用 GitHub CLI 创建仓库并推送 ===")
    auth = run(["gh", "auth", "status"], capture=True)
    if not auth or auth.returncode != 0:
        say("  gh 未登录。请先运行 `gh auth login`，或改用下面的手动方式。")
        return False
    full = repo if "/" in repo else "%s/%s" % (user, repo)
    r = run(["gh", "repo", "create", full, "--public",
             "--source=.", "--remote=origin", "--push"], capture=True)
    msg = ((r.stdout or "") + (r.stderr or "")).strip() if r else ""
    if r and r.returncode == 0:
        say("  已创建并推送：https://github.com/%s" % full)
        say("  " + msg.splitlines()[0] if msg else "")
        return True
    say("  创建失败：%s" % msg[:400])
    return False


def push_manual(user, repo):
    full = "%s/%s" % (user, repo)
    url = "https://github.com/%s.git" % full
    say("\n=== 推送到已有空仓库 ===")
    say("  目标：%s" % url)
    say("  若尚未创建：打开 https://github.com/new ，仓库名填 %s，选 Public，" % repo)
    say("  不要勾选 README / .gitignore / License（保持空仓库），然后点 Create repository。")
    say("")
    input("  确认已创建后按回车继续（Ctrl+C 取消）...")

    run(["git", "remote", "remove", "origin"], capture=True)
    r = run(["git", "remote", "add", "origin", url], capture=True)
    say("  remote 设置：%s" % ("完成" if r and r.returncode == 0 else "失败"))
    run(["git", "branch", "-M", "main"], capture=True)
    say("\n  正在推送（如弹出登录请照提示完成）...")
    r = run(["git", "push", "-u", "origin", "main"])
    if r is not None and getattr(r, "returncode", 1) == 0:
        return True
    say("\n  推送未完成。常见原因：")
    say("   - 未登录：GitHub 已不支持密码推送，请在弹出的窗口登录，")
    say("     或改用 Personal Access Token / 安装 gh 后执行 `gh auth login`。")
    say("   - 仓库非空：确认是空仓库，或先执行 git pull --rebase origin main。")
    return False


def personalize_readme(user, repo):
    """把 README 里的在线地址占位符换成真实 Pages 地址，并追加提交。"""
    p = os.path.join(HERE, "README.md")
    try:
        with open(p, "r", encoding="utf-8") as f:
            s = f.read()
        if "YOUR_USERNAME" not in s and "YOUR_REPO" not in s:
            return
        s = s.replace("YOUR_USERNAME", user).replace("YOUR_REPO", repo)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(s)
        run(["git", "add", "README.md"], capture=True)
        r = run(["git", "commit", "-m", "docs: 填入实际 GitHub Pages 地址"], capture=True)
        if r and r.returncode == 0:
            r2 = run(["git", "push", "origin", "main"], capture=True)
            if r2 and r2.returncode == 0:
                say("\n  已自动把 README 的在线地址替换为 https://%s.github.io/%s/" % (user, repo))
                return
        say("  README 地址已替换，但自动提交/推送未成功，请手动 git add/commit/push。")
    except Exception as e:
        say("  README 地址替换跳过：%s" % e)


def finish(user, repo):
    personalize_readme(user, repo)
    say("\n" + "=" * 60)
    say("推送完成，接下来只需两步即可「打开即用」：")
    say("")
    say("1) 开启在线版：")
    say("   https://github.com/%s/%s/settings/pages" % (user, repo))
    say("   Build and deployment → Source 选 GitHub Actions")
    say("   等待 Actions 跑完，访问：")
    say("   https://%s.github.io/%s/" % (user, repo))
    say("")
    say("2) 发布安装包（可选）：")
    say("   git tag v1.2.0 && git push origin v1.2.0")
    say("   自动创建 Release 并附上两个 APK。")
    say("=" * 60)


def main():
    say("IronLog · GitHub 发布助手")
    say("目录：" + HERE)

    if not precheck():
        say("\n自检未通过，已停止。")
        return 1
    if "--check" in sys.argv:
        say("\n（--check 模式：只自检，未做任何提交或推送）")
        return 0

    if not shutil.which("git"):
        say("未找到 git，请先安装 Git。")
        return 1

    if not init_and_commit():
        return 1

    say("\n=== GitHub 仓库信息 ===")
    user = input("你的 GitHub 用户名：").strip()
    if not user:
        say("已取消（未推送）。本地提交已保留。")
        return 0
    repo = input("仓库名（直接回车用 ironlog）：").strip() or "ironlog"

    pushed = False
    if shutil.which("gh"):
        ans = input("检测到 gh，是否用它自动创建仓库并推送？[Y/n] ").strip().lower()
        if ans in ("", "y", "yes"):
            pushed = push_with_gh(user, repo)
    if not pushed:
        pushed = push_manual(user, repo)

    if pushed:
        finish(user, repo)
        return 0
    say("\n本地仓库已就绪，推送完成后按上面的步骤开启 Pages 即可。")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        say("\n已取消。")
        sys.exit(130)
