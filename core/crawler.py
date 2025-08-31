"""
crawler.py
Crawler utama untuk mengambil konten HTML dari web.
Menggunakan requests atau httpx.
"""

import requests
import time
import random
from urllib.parse import urljoin, urlparse
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Crawler:
    def __init__(self, headers=None, timeout=10, delay_range=(1, 3)):
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
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


# GenericScraper: fallback universal extractor jika tidak ada plugin yang cocok
from core.parser import Parser
import re
from datetime import datetime
import json

class GenericScraper:
    def __init__(self):
        self.name = "GenericScraper"
        
    def match(self, url):
        """Selalu cocok untuk semua URL sebagai fallback."""
        return True

    def extract(self, html, url=None):
        """Ekstrak data universal dari HTML apapun."""
        parser = Parser()
        soup = parser.parse(html)
        
        data = {
            "url": url or "",
            "title": "",
            "description": "",
            "content": "",
            "images": [],
            "links": [],
            "meta_tags": {},
            "structured_data": {},
            "extracted_at": datetime.now().isoformat()
        }
        
        try:
            # Judul
            title = soup.find('title')
            data['title'] = title.get_text(strip=True) if title else ""
            
            # Meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if not meta_desc:
                meta_desc = soup.find('meta', attrs={'property': 'og:description'})
            data['description'] = meta_desc.get('content', '') if meta_desc else ""
            
            # Konten utama
            content_selectors = [
                'article', 'main', '.content', '.post-content', 
                '.entry-content', '.article-body', '#content'
            ]
            for selector in content_selectors:
                element = soup.select_one(selector)
                if element:
                    data['content'] = element.get_text(strip=True)
                    break
            
            # Gambar
            for img in soup.find_all('img'):
                src = img.get('src')
                if src:
                    data['images'].append({
                        "url": src,
                        "alt": img.get('alt', '')
                    })
            
            # Links
            for link in soup.find_all('a', href=True):
                data['links'].append({
                    "url": link['href'],
                    "text": link.get_text(strip=True)
                })
                
            # Meta tags
            for meta in soup.find_all('meta'):
                name = meta.get('name') or meta.get('property')
                content = meta.get('content')
                if name and content:
                    data['meta_tags'][name] = content
                    
        except Exception as e:
            logger.error(f"Error extracting data: {str(e)}")
            
        return data
        
    def format(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format data untuk output"""
        return data
