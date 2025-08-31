"""
universal_scraper.py
Universal web scraper yang dapat menangani berbagai jenis website
"""

import requests
import time
import random
import json
import re
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logger = logging.getLogger(__name__)

class UniversalScraper:
    """Scraper universal untuk semua jenis website"""
    
    def __init__(self, use_selenium=False, headers=None, timeout=30):
        self.use_selenium = use_selenium
        self.timeout = timeout
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        self.driver = None
        
    def __enter__(self):
        if self.use_selenium:
            self._setup_selenium()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()
            
    def _setup_selenium(self):
        """Setup Selenium WebDriver untuk JavaScript-heavy sites"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(f"--user-agent={self.headers['User-Agent']}")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_page_load_timeout(self.timeout)
        
    def fetch_page(self, url: str) -> str:
        """Ambil konten HTML dari URL dengan requests atau Selenium"""
        try:
            if self.use_selenium and self.driver:
                self.driver.get(url)
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                time.sleep(random.uniform(2, 4))  # Tunggu konten dimuat
                return self.driver.page_source
            else:
                response = requests.get(
                    url, 
                    headers=self.headers, 
                    timeout=self.timeout,
                    allow_redirects=True
                )
                response.raise_for_status()
                return response.text
                
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None
            
    def extract_universal_data(self, html: str, url: str) -> Dict[str, Any]:
        """Ekstrak data universal dari HTML apapun"""
        if not html:
            return {}
            
        soup = BeautifulSoup(html, 'lxml')
        
        # Struktur data hasil ekstraksi
        data = {
            "url": url,
            "title": self._extract_title(soup),
            "description": self._extract_description(soup),
            "content": self._extract_main_content(soup),
            "images": self._extract_images(soup, url),
            "links": self._extract_links(soup, url),
            "meta_tags": self._extract_meta_tags(soup),
            "structured_data": self._extract_structured_data(soup),
            "text_content": self._extract_text_content(soup),
            "headings": self._extract_headings(soup),
            "tables": self._extract_tables(soup),
            "lists": self._extract_lists(soup),
            "forms": self._extract_forms(soup),
            "social_media": self._extract_social_links(soup),
            "contact_info": self._extract_contact_info(soup),
            "extracted_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return data
        
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Ekstrak judul halaman"""
        title_selectors = [
            'title',
            'h1',
            'meta[property="og:title"]',
            'meta[name="twitter:title"]',
            '[data-testid="headline"]',
            '.article-title',
            '.post-title',
            '.entry-title'
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                if element.name == 'meta':
                    return element.get('content', '').strip()
                else:
                    return element.get_text(strip=True)
        return ""
        
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Ekstrak deskripsi halaman"""
        desc_selectors = [
            'meta[name="description"]',
            'meta[property="og:description"]',
            'meta[name="twitter:description"]',
            'meta[name="abstract"]',
            '.summary',
            '.excerpt',
            '.lead'
        ]
        
        for selector in desc_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get('content', element.get_text()).strip()
        return ""
        
    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """Ekstrak konten utama artikel"""
        content_selectors = [
            'article',
            'main',
            '[role="main"]',
            '.content',
            '.post-content',
            '.entry-content',
            '.article-body',
            '.main-content',
            '#content',
            '.text'
        ]
        
        for selector in content_selectors:
            element = soup.select_one(selector)
            if element:
                return self._clean_text(element.get_text())
                
        # Fallback: ambil semua paragraf
        paragraphs = soup.find_all('p')
        return self._clean_text(' '.join([p.get_text() for p in paragraphs]))
        
    def _extract_images(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        """Ekstrak semua gambar"""
        images = []
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
            if src:
                full_url = urljoin(base_url, src)
                images.append({
                    "url": full_url,
                    "alt": img.get('alt', ''),
                    "title": img.get('title', '')
                })
        return images
        
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        """Ekstrak semua link"""
        links = []
        for link in soup.find_all('a', href=True):
            full_url = urljoin(base_url, link['href'])
            links.append({
                "url": full_url,
                "text": link.get_text(strip=True),
                "title": link.get('title', '')
            })
        return links
        
    def _extract_meta_tags(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Ekstrak semua meta tags"""
        meta_tags = {}
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property') or meta.get('http-equiv')
            content = meta.get('content')
            if name and content:
                meta_tags[name] = content
        return meta_tags
        
    def _extract_structured_data(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Ekstrak JSON-LD dan microdata"""
        structured_data = {
            "json_ld": [],
            "microdata": [],
            "open_graph": {},
            "twitter_card": {}
        }
        
        # JSON-LD
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                data = json.loads(script.string)
                structured_data["json_ld"].append(data)
            except:
                pass
                
        # Open Graph
        for og in soup.find_all('meta', property=re.compile(r'^og:')):
            structured_data["open_graph"][og['property'][3:]] = og.get('content', '')
            
        # Twitter Card
        for tw in soup.find_all('meta', attrs={'name': re.compile(r'^twitter:')}):
            structured_data["twitter_card"][tw['name'][8:]] = tw.get('content', '')
            
        return structured_data
        
    def _extract_text_content(self, soup: BeautifulSoup) -> str:
        """Ekstrak semua teks dari halaman"""
        return self._clean_text(soup.get_text())
        
    def _extract_headings(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Ekstrak semua heading tags"""
        headings = {}
        for level in range(1, 7):
            tags = soup.find_all(f'h{level}')
            headings[f'h{level}'] = [tag.get_text(strip=True) for tag in tags]
        return headings
        
    def _extract_tables(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Ekstrak data dari tabel"""
        tables = []
        for table in soup.find_all('table'):
            rows = []
            for tr in table.find_all('tr'):
                cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
                if cells:
                    rows.append(cells)
            tables.append({
                "headers": rows[0] if rows else [],
                "rows": rows[1:] if len(rows) > 1 else []
            })
        return tables
        
    def _extract_lists(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Ekstrak data dari list (ul, ol, dl)"""
        lists = {
            "unordered": [],
            "ordered": [],
            "definition": []
        }
        
        # Unordered lists
        for ul in soup.find_all('ul'):
            items = [li.get_text(strip=True) for li in ul.find_all('li')]
            lists["unordered"].extend(items)
            
        # Ordered lists
        for ol in soup.find_all('ol'):
            items = [li.get_text(strip=True) for li in ol.find_all('li')]
            lists["ordered"].extend(items)
            
        return lists
        
    def _extract_forms(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Ekstrak informasi form"""
        forms = []
        for form in soup.find_all('form'):
            form_data = {
                "action": form.get('action', ''),
                "method": form.get('method', 'get').upper(),
                "inputs": []
            }
            
            for input_tag in form.find_all(['input', 'textarea', 'select']):
                input_info = {
                    "type": input_tag.get('type', input_tag.name),
                    "name": input_tag.get('name', ''),
                    "value": input_tag.get('value', ''),
                    "placeholder": input_tag.get('placeholder', '')
                }
                form_data["inputs"].append(input_info)
                
            forms.append(form_data)
        return forms
        
    def _extract_social_links(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Ekstrak link social media"""
        social_patterns = {
            "facebook": r'facebook\.com',
            "twitter": r'twitter\.com|x\.com',
            "instagram": r'instagram\.com',
            "linkedin": r'linkedin\.com',
            "youtube": r'youtube\.com|youtu\.be',
            "tiktok": r'tiktok\.com'
        }
        
        social_links = {platform: [] for platform in social_patterns}
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            for platform, pattern in social_patterns.items():
                if re.search(pattern, href, re.IGNORECASE):
                    social_links[platform].append(href)
                    
        return social_links
        
    def _extract_contact_info(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Ekstrak informasi kontak"""
        contact_info = {
            "emails": [],
            "phones": [],
            "addresses": []
        }
        
        # Email patterns
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        text = soup.get_text()
        emails = re.findall(email_pattern, text)
        contact_info["emails"] = list(set(emails))
        
        # Phone patterns
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        contact_info["phones"] = list(set([p[0] + p[1] + p[2] + p[3] if isinstance(p, tuple) else p for p in phones]))
        
        return contact_info
        
    def _clean_text(self, text: str) -> str:
        """Bersihkan teks dari whitespace berlebih"""
        if not text:
            return ""
        return ' '.join(text.split())
