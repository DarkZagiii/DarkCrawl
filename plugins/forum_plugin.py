"""
Plugin untuk scraping forum diskusi.
"""

class ForumPlugin:
    def match(self, url):
        return "forum" in url or "thread" in url

    def extract(self, html):
        # Ekstrak judul thread, isi, user, tanggal
        pass

    def format(self, data):
        return {
            "judul": data.get("title"),
            "isi": data.get("body"),
            "user": data.get("user"),
            "tanggal": data.get("date"),
        }
