#!/usr/bin/env python3
"""
Lazada scraper - CLEAN VERSION
Dengan filtering untuk remove navigation items dan hanya ambil real products
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re
import time
import json

def is_real_product(text):
    """Check jika text adalah benar-benar nama produk"""
    
    # Reject navigation/UI elements
    reject_patterns = [
        'Chat', 'Help', 'Admin', 'Seller', 'Daftar', 'Login', 'items found',
        'Pusat', 'MENJADI', 'Live Chat', 'Klik', 'Urutkan', 'Instant Delivery',
        'Lowest Price', 'Voucher', 'Diskon', 'Panel Akun', 'Belanja', 'INTERNAL',
        'Masukan', 'FEEDBACK', 'banyak untung', 'Hanya Untuk', 'Pal', 'Filter',
        'Kategori', 'Lokasi', 'Kota', 'Provinsi', 'Pengiriman', 'Grosir',
        'Jenis', 'Garansi', 'Kota Jakarta', 'Kab.', 'Pulsa', 'Tagihan',
        'Mobile Top Up', 'Bill Payment', 'Flash Deal', 'Branded', 'Authenticity'
    ]
    
    for pattern in reject_patterns:
        if pattern.lower() in text.lower():
            return False
    
    # Accept if it looks like product (has brand names or product-like terms)
    accept_patterns = [
        'laptop', 'notebook', 'asus', 'lenovo', 'hp', 'acer', 'dell', 'toshiba',
        'ram', 'ssd', 'inch', 'gb', 'core', 'intel', 'amd', 'processor',
        'ryzen', 'celeron', 'pentium', 'windows', 'chromebook', 'gaming',
        'ultrabook', 'netbook', 'touchscreen'
    ]
    
    text_lower = text.lower()
    has_product_indicator = any(term in text_lower for term in accept_patterns)
    
    if has_product_indicator:
        return True
    
    return False

def scrape_lazada_clean(keyword="laptop"):
    """Extract REAL products dari Lazada dengan filtering"""
    
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    print("=" * 80)
    print("🛒 LAZADA SCRAPER - CLEAN VERSION")
    print("=" * 80)
    
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        url = f"https://www.lazada.co.id/catalog/?q={keyword}"
        print(f"\n[*] Loading: {url}")
        driver.get(url)
        
        print("[*] Waiting for page to render...")
        time.sleep(5)
        
        # Scroll to load more products
        print("[*] Scrolling to load products...")
        for i in range(8):
            driver.execute_script("window.scrollBy(0, 600);")
            time.sleep(0.3)
        
        # Get full text
        text_content = driver.execute_script("return document.body.innerText;")
        print(f"[✓] Page loaded with {len(text_content):,} characters")
        
        # Extract products
        print("\n[*] Extracting and filtering products...")
        products = []
        lines = text_content.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            if not line or len(line) < 15 or len(line) > 200:
                continue
            
            # Check if it's a real product
            if not is_real_product(line):
                continue
            
            # Skip duplicates
            if line in [p['name'] for p in products]:
                continue
            
            # Find next price
            price = "N/A"
            for j in range(i+1, min(i+10, len(lines))):
                if 'Rp' in lines[j]:
                    price_match = re.search(r'Rp[\s\d.,]+', lines[j])
                    if price_match:
                        price = price_match.group(0).strip()
                    break
            
            products.append({
                'name': line,
                'price': price,
                'platform': 'Lazada'
            })
        
        # Limit to top 20
        products = products[:20]
        
        print(f"\n[✓] Successfully extracted {len(products)} real products")
        
        # Display
        print("\n" + "=" * 80)
        print("📦 LAZADA PRODUCTS")
        print("=" * 80)
        
        for idx, prod in enumerate(products, 1):
            print(f"\n{idx}. {prod['name']}")
            print(f"   💰 {prod['price']}")
        
        return products
        
    except Exception as e:
        print(f"\n[✗] Error: {e}")
        import traceback
        traceback.print_exc()
        return []
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    products = scrape_lazada_clean("laptop")
    
    print("\n" + "=" * 80)
    print(f"✅ RESULT: {len(products)} real products extracted from Lazada")
    print("=" * 80)
    print(json.dumps(products, indent=2, ensure_ascii=False))
