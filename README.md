# 邮箱验证码批量解析

本地启动一个小服务，批量解析 邮箱----链接 格式的接口，提取邮件里的验证码。

## 给最终用户

下载 `邮箱验证码解析-Windows.zip` -> 解压 -> 双击 `邮箱验证码解析.exe`，浏览器自动打开。
不需要装 Python。

## 给开发者

### 本地运行（任意系统，需要 Python 3）

```bash
python3 server.py
```

终端会打印 `http://localhost:8001`，浏览器访问即可。

### 通过 GitHub Actions 自动构建 Windows exe

1. 把这个目录初始化成 git 仓库并推到 GitHub：

   ```bash
   cd mail-parser-app
   git init
   git add .
   git commit -m "init"
   git branch -M main
   git remote add origin git@github.com:你的用户名/仓库名.git
   git push -u origin main
   ```

2. 第一次 push 后，GitHub 仓库的 Actions 标签页会自动跑构建。
   - 跑完点进 workflow run，最下面 Artifacts 区域有 `邮箱验证码解析-Windows.zip`，下载即可。

3. 想让构建产物直接发布到 Releases 页（更适合给别人下载链接），打 tag：

   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

   tag 推上去后会自动创建一个 GitHub Release，附带 zip 下载。

### 修改后重新构建

改了代码后：

```bash
git add .
git commit -m "update"
git push
```

push 后 Actions 自动重新打包。要发新版本就再打个新 tag（v1.0.1, v1.0.2 ...）。

## 文件说明

- `server.py` - 本地 HTTP 服务，托管网页 + 反向代理（绕过浏览器跨域）
- `outlook邮箱管理.html` - 网页本身，所有 UI 和解析逻辑
- `.github/workflows/build.yml` - GitHub Actions 构建配置

## 用法

输入框每行粘贴 `邮箱----链接`，点开始解析。详细使用见 `README.txt`。
