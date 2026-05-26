"""
本地启动:  python3 server.py   (Windows 用 python server.py)
然后看终端打印的地址, 一般是 http://localhost:8001
"""

import http.server
import socketserver
import urllib.parse
import urllib.request
import urllib.error
import ssl
import sys
import os
import threading
import webbrowser
import traceback
from pathlib import Path

PORTS = [8001, 8002, 8003, 8004, 8005, 8010, 8080, 8123]

if getattr(sys, "frozen", False):
    ROOT = Path(sys._MEIPASS)
else:
    ROOT = Path(__file__).resolve().parent

INDEX = "outlook邮箱管理.html"


def out(msg):
    print(msg, flush=True)


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/proxy":
            qs = urllib.parse.parse_qs(parsed.query)
            target = (qs.get("url") or [""])[0]
            self.proxy(target)
            return
        if parsed.path in ("/", ""):
            self.path = "/" + urllib.parse.quote(INDEX)
        return super().do_GET()

    def proxy(self, target):
        if not target or not target.startswith(("http://", "https://")):
            self._send_text(400, "missing or invalid url param")
            return
        try:
            req = urllib.request.Request(
                target,
                headers={
                    "User-Agent": self.headers.get("User-Agent", "Mozilla/5.0"),
                    "Accept": "*/*",
                },
            )
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
                body = resp.read()
                self.send_response(resp.status)
                ct = resp.headers.get("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Type", ct)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
        except urllib.error.HTTPError as e:
            body = e.read() if e.fp else b""
            self.send_response(e.code)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except Exception as e:
            self._send_text(502, f"proxy error: {e}")

    def _send_text(self, code, msg):
        body = msg.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        sys.stderr.write("[server] " + (fmt % args) + "\n")
        sys.stderr.flush()


def hold_on_exit():
    if os.name == "nt":
        try:
            input("\n按回车键关闭窗口...")
        except EOFError:
            pass


def main():
    out(f"Python: {sys.version.split()[0]}")
    out(f"工作目录: {ROOT}")
    if not (ROOT / INDEX).exists():
        out(f"[错误] 找不到 {INDEX}, 请确认 server.py 和 html 放在同一目录")
        hold_on_exit()
        sys.exit(1)

    socketserver.TCPServer.allow_reuse_address = True
    last_err = None
    for port in PORTS:
        try:
            httpd = socketserver.TCPServer(("127.0.0.1", port), Handler)
        except OSError as e:
            out(f"端口 {port} 不可用: {e}")
            last_err = e
            continue
        out("=" * 50)
        out(f"启动成功! 浏览器打开: http://localhost:{port}")
        out("按 Ctrl+C 停止")
        out("=" * 50)
        threading.Timer(1.0, lambda: webbrowser.open(f"http://localhost:{port}")).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            out("\n已停止")
        finally:
            httpd.server_close()
        return
    out(f"[错误] 所有备选端口都被占用了, 最后错误: {last_err}")
    hold_on_exit()
    sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        hold_on_exit()
        sys.exit(1)
