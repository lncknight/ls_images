"""Run inside the image: python3 /path/to/check_waf.py (no external services)."""

import http.server
import json
from pathlib import Path
import socket
import subprocess
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request


class Backend(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

    def do_POST(self):
        self.rfile.read(int(self.headers.get("Content-Length", 0)))
        self.do_GET()

    def log_message(self, *args):
        pass


def check():
    backend = http.server.HTTPServer(("127.0.0.1", 0), Backend)
    threading.Thread(target=backend.serve_forever, daemon=True).start()
    try:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.chmod(0o755)
            with socket.socket() as listener:
                listener.bind(("127.0.0.1", 0))
                port = listener.getsockname()[1]

            for mode in ("DetectionOnly", "On"):
                # Use the shipped engine setting unchanged for the default check.
                override = "" if mode == "DetectionOnly" else "SecRuleEngine On"
                rules = root / "rules.conf"
                rules.write_text(f"Include /etc/modsecurity/main.conf\n{override}\n"
                                 f"SecAuditLog {root}/audit.log\n")
                config = root / "nginx.conf"
                config.write_text(f"""
include /etc/modsecurity/nginx-main.conf;
user nginx;
pid {root}/nginx.pid;
error_log {root}/error.log notice;
events {{ worker_connections 64; }}
http {{
    access_log off;
    client_max_body_size 20m;
    modsecurity on;
    modsecurity_rules_file {rules};
    server {{
        listen 127.0.0.1:{port};
        server_name localhost;
        location / {{ proxy_pass http://127.0.0.1:{backend.server_port}; }}
    }}
}}
""")
                process = subprocess.Popen(["nginx", "-c", str(config), "-g", "daemon off;"])
                try:
                    url = f"http://127.0.0.1:{port}/"
                    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

                    def request(path="", data=None, content_type=None):
                        headers = {"Content-Type": content_type} if content_type else {}
                        req = urllib.request.Request(url + path, data=data, headers=headers)
                        try:
                            with opener.open(req, timeout=10) as response:
                                return response.status
                        except urllib.error.HTTPError as error:
                            return error.code

                    for _ in range(100):
                        if process.poll() is not None:
                            raise RuntimeError("nginx exited before accepting requests")
                        try:
                            assert request() == 200
                            break
                        except urllib.error.URLError:
                            time.sleep(0.05)
                    else:
                        raise RuntimeError("nginx did not become ready")

                    assert request("?" + urllib.parse.urlencode({"q": "O'Reilly's dinner"})) == 200
                    assert request(data=b'{"bio":"I love dinners and music"}',
                                   content_type="application/json") == 200
                    assert request(data=urllib.parse.urlencode({"name": "O'Reilly"}).encode(),
                                   content_type="application/x-www-form-urlencoded") == 200
                    # Guard against the recommended config's 128 KiB non-file limit.
                    assert request(data=b'{"bio":"' + b"a" * 140000 + b'"}',
                                   content_type="application/json") == 200
                    boundary = "WafSmokeBoundary"
                    upload = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"photo\"; "
                              f"filename=\"sample.txt\"\r\nContent-Type: text/plain\r\n\r\n"
                              f"sample upload\r\n--{boundary}--\r\n").encode()
                    assert request(data=upload, content_type=f"multipart/form-data; boundary={boundary}") == 200

                    attack = "1' OR '1'='1' -- "
                    expected = 200 if mode == "DetectionOnly" else 403

                    def assert_sqli(path="", data=None, content_type=None):
                        audit_path = root / "audit.log"
                        offset = audit_path.stat().st_size if audit_path.exists() else 0
                        assert request(path, data, content_type) == expected
                        for _ in range(100):
                            record = audit_path.read_text()[offset:] if audit_path.exists() else ""
                            if "942" in record and "SQL" in record:
                                break
                            time.sleep(0.01)
                        else:
                            raise AssertionError("SQL injection rule did not audit this request")

                    assert_sqli("?" + urllib.parse.urlencode({"id": attack}))
                    for media_type in ("application/json", "application/problem+json"):
                        assert_sqli(data=json.dumps({"id": attack}).encode(), content_type=media_type)
                finally:
                    process.terminate()
                    process.wait(timeout=10)
                    if (root / "error.log").exists():
                        print((root / "error.log").read_text())
                audit = (root / "audit.log").read_text()
                assert "942" in audit, "SQL injection rule did not leave audit evidence"
                assert "SQL" in audit, "SQL injection detection message missing"
                (root / "audit.log").unlink()
                print(f"PASS: {mode}: benign requests accepted; SQLi status={expected}, audited")
    finally:
        backend.shutdown()
        backend.server_close()


if __name__ == "__main__":
    check()
