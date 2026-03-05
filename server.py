#!/usr/bin/env python3
"""GeoMap dev server — serves static files + proxies webcam images.

The MapTiler API key is read from .env (gitignored) at startup and served
as /config.js so it never needs to be hardcoded in index.html.
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import urllib.request
import os

PORT = 8900

# ── Read API key from .env ─────────────────────────────────────────────────
def load_env(path='.env'):
    env = {}
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    env[k.strip()] = v.strip()
    except FileNotFoundError:
        pass
    return env

_env = load_env()
API_KEY = _env.get('apiKey', '')
if not API_KEY:
    print('⚠️  WARNING: apiKey not found in .env — map tiles will not load.')

CONFIG_JS = f'const API_KEY = "{API_KEY}";\n'.encode()

# ── Proxy security: only fetch from these hosts ────────────────────────────
ALLOWED_HOSTS = {'www.foto-webcam.eu', 'foto-webcam.eu'}

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # ── Serve API key as a JS config module ───────────────────────────
        if self.path in ('/config.js', '/config.js?'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/javascript')
            self.send_header('Content-Length', str(len(CONFIG_JS)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(CONFIG_JS)
            return

        # ── Proxy webcam images ────────────────────────────────────────────
        if self.path.startswith('/proxy/'):
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            target = params.get('url', [None])[0]

            if not target:
                self.send_error(400, 'Missing ?url= parameter')
                return

            # Security: allowlist check
            target_host = urlparse(target).hostname or ''
            if target_host not in ALLOWED_HOSTS:
                self.send_error(403, f'Host not allowed: {target_host}')
                return

            # Security: HTTPS only
            if not target.startswith('https://'):
                self.send_error(403, 'Only HTTPS targets are allowed')
                return

            try:
                req = urllib.request.Request(target, headers={
                    'User-Agent': 'Mozilla/5.0 (compatible; GeoMapProxy/1.0)',
                    'Referer': 'https://www.foto-webcam.eu/',
                })
                with urllib.request.urlopen(req, timeout=10) as resp:
                    content_type = resp.headers.get('Content-Type', '')
                    if 'image' not in content_type:
                        self.send_error(502, 'Upstream did not return an image')
                        return
                    data = resp.read()
                self.send_response(200)
                self.send_header('Content-Type', 'image/jpeg')
                self.send_header('Content-Length', str(len(data)))
                self.send_header('Cache-Control', 'no-store')
                self.send_header('Access-Control-Allow-Origin', 'http://localhost:8900')
                self.end_headers()
                self.wfile.write(data)
            except Exception as e:
                self.send_error(502, str(e))
            return

        super().do_GET()

    def log_message(self, fmt, *args):

        if not self.path.startswith('/proxy/'):
            super().log_message(fmt, *args)

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    httpd = HTTPServer(('', PORT), Handler)
    print(f'GeoMap → http://localhost:{PORT}')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nStopped.')
