"""
Plugin untuk scraping situs e-commerce.
"""

class EcommercePlugin:
    def match(self, url):
        return "tokopedia" in url or "shopee" in url or "ecommerce" in url

    def extract(self, html=None, url=None):
        """
        Jika url diberikan, gunakan Selenium untuk scraping Shopee (JS rendered). Jika hanya html, fallback ke BeautifulSoup.
        """
        try:
            if url:
                from selenium import webdriver
                from selenium.webdriver.chrome.options import Options
                from selenium.webdriver.common.by import By
                from webdriver_manager.chrome import ChromeDriverManager
                import time
                options = Options()
                options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
                driver.get(url)
                time.sleep(5)  # Tunggu JS render
                products = []
                items = driver.find_elements(By.CSS_SELECTOR, "div.shopee-search-item-result__item")
                for item in items:
                    try:
                        name = item.find_element(By.CSS_SELECTOR, "div._10Wbs-").text
                        price = item.find_element(By.CSS_SELECTOR, "span._1xk7ak").text
                        products.append({"name": name, "price": price, "desc": name})
                    except Exception:
                        continue
                driver.quit()
                return products[0] if products else None
        except Exception as e:
            print(f"[EcommercePlugin][Selenium] Error: {e}")
        # Fallback ke BeautifulSoup jika html diberikan
        if html:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, "lxml")
            products = []
            for item in soup.find_all("div", class_=lambda x: x and "shopee-search-item-result__item" in x):
                name = item.find("div", class_=lambda x: x and "_10Wbs-" in x)
                price = item.find("span", class_=lambda x: x and "_1xk7ak" in x)
                desc = name.text.strip() if name else ""
                price_val = price.text.strip() if price else ""
                products.append({
                    "name": desc,
                    "price": price_val,
                    "desc": desc,
                })
            if not products:
                for a in soup.find_all("a", href=True):
                    if "/product/" in a["href"]:
                        name = a.get_text(strip=True)
                        products.append({"name": name, "price": "", "desc": name})
            return products[0] if products else None
        return None

    def format(self, data):
        return {
            "nama": data.get("name"),
            "harga": data.get("price"),
            "deskripsi": data.get("desc"),
        }
