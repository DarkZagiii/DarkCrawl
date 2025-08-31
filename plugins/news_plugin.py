"""
Plugin untuk scraping situs berita atau blog.
"""

class NewsPlugin:
    def match(self, url):
        return "news" in url or "blog" in url

    def extract(self, html):
        from bs4 import BeautifulSoup
        import re
        soup = BeautifulSoup(html, "lxml")
        # Judul
        title = soup.title.string.strip() if soup.title and soup.title.string else ""
        # Isi utama (ambil <article> atau <main> atau <body>)
        main = soup.find('article') or soup.find('main') or soup.find('body')
        body = main.get_text(separator='\n', strip=True) if main else ""
        # Tanggal (meta atau pola tanggal)
        date = ""
        for meta in soup.find_all('meta'):
            if meta.get('name', '').lower() in ['date', 'pubdate', 'publishdate', 'og:pubdate']:
                date = meta.get('content', '')
                break
            if meta.get('property', '').lower() in ['article:published_time', 'og:published_time']:
                date = meta.get('content', '')
                break
        if not date:
            match = re.search(r'(\d{4}-\d{2}-\d{2})', body)
            if match:
                date = match.group(1)
        return {"title": title, "body": body, "date": date}

    def format(self, data):
        return {
            "judul": data.get("title"),
            "isi": data.get("body"),
            "tanggal": data.get("date"),
        }
