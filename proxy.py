#!/usr/bin/env python3
"""
AI Wallpaper Proxy - 代理 Pollinations.ai 图片请求
服务器端下载图片 → 返回给浏览器，绕过浏览器网络限制
"""
import http.server
import urllib.request
import urllib.parse
import urllib.error
import time
import sys
import os
import json

PORT = 8889
POLLINATIONS = "https://image.pollinations.ai/prompt/"
MAX_RETRIES = 10
RETRY_DELAY = 4

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stderr.write("[%s] %s\n" % (time.strftime("%H:%M:%S"), fmt % args))

    def do_GET(self):
        path = self.path
        if path.startswith("/proxy"):
            self.handle_proxy(path)
        elif path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()

    def handle_proxy(self, path):
        try:
            qs = path.split("?", 1)[1] if "?" in path else ""
            params = urllib.parse.parse_qs(qs)

            prompt = params.get("prompt", [""])[0]
            width = params.get("w", ["512"])[0]
            height = params.get("h", ["512"])[0]
            seed = params.get("seed", [str(int(time.time()))])[0]

            if not prompt:
                self.send_json({"error": "prompt is required"}, 400)
                return

            encoded = urllib.parse.quote(prompt)
            url = "%s%s?width=%s&height=%s&nologo=true&seed=%s" % (
                POLLINATIONS, encoded, width, height, seed
            )

            print("[proxy] %s" % url, file=sys.stderr)

            # Retry loop
            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    req = urllib.request.Request(url, headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                    })
                    resp = urllib.request.urlopen(req, timeout=30)
                    content_type = resp.headers.get("Content-Type", "")
                    data = resp.read()

                    if content_type.startswith("image/") and len(data) > 100:
                        self.send_response(200)
                        self.send_header("Content-Type", content_type)
                        self.send_header("Content-Length", str(len(data)))
                        self.send_header("Cache-Control", "public, max-age=3600")
                        self.send_header("Access-Control-Allow-Origin", "*")
                        self.end_headers()
                        self.wfile.write(data)
                        print("[proxy] OK attempt=%d size=%d" % (attempt, len(data)), file=sys.stderr)
                        return
                    else:
                        print("[proxy] not-image attempt=%d type=%s size=%d" % (
                            attempt, content_type, len(data)), file=sys.stderr)
                except Exception as e:
                    print("[proxy] err attempt=%d: %s" % (attempt, e), file=sys.stderr)

                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY)

            self.send_json({"error": "generation timeout after %d retries" % MAX_RETRIES}, 504)

        except Exception as e:
            print("[proxy] fatal: %s" % e, file=sys.stderr)
            self.send_json({"error": str(e)}, 500)

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()


if __name__ == "__main__":
    print("AI Wallpaper Proxy starting on port %d..." % PORT, file=sys.stderr)
    server = http.server.HTTPServer(("0.0.0.0", PORT), ProxyHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...", file=sys.stderr)
        server.shutdown()
