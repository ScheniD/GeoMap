#!/usr/bin/env python3
"""GeoMap dev server — serves static files + proxies webcam images."""

from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import urllib.request
import os

PORT = 8900

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # /proxy/?url=https://... — fetch the image server-side
        if self.path.startswith('/proxy/'):
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            target = params.get('url', [None])[0]
            if not target:
                self.send_error(400, 'Missing ?url= parameter')
                return
            try:
                req = urllib.request.Request(target, headers={
                    'User-Agent': 'Mozilla/5.0 (compatible; GeoMapProxy/1.0)',
                    # Spoof referer so foto-webcam.eu hotlink check passes
                    'Referer': 'https://www.foto-webcam.eu/',
                })
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = resp.read()
                self.send_response(200)
                self.send_header('Content-Type', 'image/jpeg')
                self.send_header('Content-Length', str(len(data)))
                self.send_header('Cache-Control', 'no-store')
                # Allow JS on the page to use the response
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(data)
            except Exception as e:
                self.send_error(502, str(e))
        else:
            super().do_GET()

    def log_message(self, fmt, *args):
        # Only log non-proxy requests to keep console clean
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
