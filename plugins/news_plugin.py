"""
Plugin untuk scraping situs berita atau blog.
"""

class NewsPlugin:
    def match(self, url):
        return "news" in url or "blog" in url

    def extract(self, html):
        # Extract judul, isi artikel, tanggal
        pass

    def format(self, data):
        return {
            "judul": data.get("title"),
            "isi": data.get("body"),
            "tanggal": data.get("date"),
        }
