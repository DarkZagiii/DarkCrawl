"""
crawler.py
Crawler utama untuk mengambil konten HTML dari web.
Menggunakan requests atau httpx.
"""

import requests

class Crawler:
    def __init__(self, headers=None, timeout=10):
        self.headers = headers or {"User-Agent": "Mozilla/5.0 (compatible; AI-Scraper/1.0)"}
        self.timeout = timeout

    def fetch(self, url):
        """Ambil konten HTML dari URL."""
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"[Crawler] Gagal mengambil {url}: {e}")
            return None
