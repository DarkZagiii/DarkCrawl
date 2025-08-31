"""
Plugin untuk scraping forum diskusi.
"""

class ForumPlugin:
    def match(self, url):
        return "forum" in url or "thread" in url

    def extract(self, html):
        from bs4 import BeautifulSoup
        import re
        soup = BeautifulSoup(html, "lxml")
        # Judul thread
        title = soup.title.string.strip() if soup.title and soup.title.string else ""
        # Isi utama thread (ambil <article> atau <main> atau <body>)
        main = soup.find('article') or soup.find('main') or soup.find('body')
        body = main.get_text(separator='\n', strip=True) if main else ""
        # User (ambil dari <meta> atau <span class="user">)
        user = ""
        user_meta = soup.find('meta', {'name': 'author'})
        if user_meta:
            user = user_meta.get('content', '')
        if not user:
            user_span = soup.find('span', class_=lambda x: x and 'user' in x)
            if user_span:
                user = user_span.get_text(strip=True)
        # Tanggal
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
        return {"title": title, "body": body, "user": user, "date": date}

    def format(self, data):
        return {
            "judul": data.get("title"),
            "isi": data.get("body"),
            "user": data.get("user"),
            "tanggal": data.get("date"),
        }
