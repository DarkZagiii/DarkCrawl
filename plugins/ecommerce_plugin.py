"""
Plugin untuk scraping situs e-commerce.
"""

class EcommercePlugin:
    def match(self, url):
        return "tokopedia" in url or "shopee" in url or "ecommerce" in url

    def extract(self, html):
        # Ekstrak nama produk, harga, deskripsi, dsb
        pass

    def format(self, data):
        return {
            "nama": data.get("name"),
            "harga": data.get("price"),
            "deskripsi": data.get("desc"),
        }
