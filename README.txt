# Outlook 邮箱验证码批量解析 (本地版)

## Windows 用户 (推荐)
1. 解压全部文件到一个文件夹
2. 双击 启动.bat
3. 黑窗口里会显示 "启动成功! 浏览器打开: http://localhost:8001" 之类的地址
4. 浏览器输入那个地址访问

如果黑窗口提示没装 Python:
- 去 https://www.python.org/downloads/ 下载安装
- 安装时一定勾选 "Add python.exe to PATH"
- 装完重新双击 启动.bat

## Mac / Linux 用户
打开终端, cd 到解压出来的目录, 运行:
  python3 server.py

## 常见问题
Q: 双击 server.py 黑窗口闪一下就关了?
A: 请改用 启动.bat (Windows), 或在终端 cd 到目录用命令运行, 这样能看到错误信息

Q: 提示端口被占用?
A: 脚本会自动尝试 8001 / 8002 / 8003 / ... / 8080 / 8123, 看终端打印出来的实际地址

Q: failed to fetch?
A: 必须通过 http://localhost:xxxx 访问, 不能双击 html. 服务必须保持运行 (黑窗口别关)

## 文件
- outlook邮箱管理.html  网页本身
- server.py             本地服务 (托管网页 + 反代绕过浏览器跨域)
- 启动.bat              Windows 一键启动

## 用法
1. 输入框每行粘贴一条 邮箱----链接, 也支持逗号或制表符分隔
2. 点 "开始解析", 自动并发抓取邮件并提取验证码
3. 点 "+ 新建分组" 给邮箱归类, 每条记录上的标签可点选切换分组
4. 数据存在浏览器 localStorage, 关页面不丢
