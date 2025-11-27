#!/usr/bin/env python3
"""
Tokopedia Scraper - Smart Text-Based Extraction
Extracts products and prices using intelligent text parsing
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import time
import json
import sys

def scrape_tokopedia_smart(keyword="laptop"):
    """Extract products from Tokopedia using smart text parsing"""
    
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    print("=" * 80)
    print("🛒 TOKOPEDIA SCRAPER - SMART EXTRACTION")
    print("=" * 80)
    
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        url = f"https://www.tokopedia.com/search?q={keyword}"
        print(f"\n[*] Loading: {url}")
        driver.get(url)
        
        print("[*] Waiting for page to load...")
        time.sleep(5)
        
        # Scroll multiple times
        print("[*] Scrolling to load products...")
        for i in range(8):
            driver.execute_script("window.scrollBy(0, 600);")
            time.sleep(0.3)
        
        # Get text content
        text_content = driver.execute_script("return document.body.innerText;")
        
        print(f"[✓] Page loaded: {len(text_content):,} characters")
        
        # Extract products
        print("\n[*] Parsing products with prices...")
        products = []
        
        lines = text_content.split('\n')
        
        # Find all prices
        all_prices = re.findall(r'Rp[\s\.,0-9]+', text_content)
        print(f"[*] Found {len(all_prices)} prices in page")
        
        # Parse products with heuristics
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Skip empty or too short
            if not line or len(line) < 15 or len(line) > 200:
                continue
            
            # Skip known navigation items
            if any(skip in line for skip in ['Tokopedia', 'Kategori', 'Keranjang', 'Akun', 'Wishlist',
                                             'Chat', 'Help', 'Pengiriman', 'filter', 'Urutkan',
                                             'Cashback', 'Gratis Ongkos', 'Official Store']):
                continue
            
            # Skip if it's just numbers/special chars
            if line.replace('.', '').replace(',', '').isdigit():
                continue
            
            # Skip duplicates
            if line in [p['name'] for p in products]:
                continue
            
            # Heuristic: This looks like a product
            # Must contain alphabetic chars and be a reasonable product name
            if (line.count(' ') >= 1 and  # At least 2 words
                any(c.isalpha() for c in line)):  # Has letters
                
                # Find next price
                price = "N/A"
                for j in range(i+1, min(i+15, len(lines))):
                    if 'Rp' in lines[j]:
                        price_match = re.search(r'Rp[\s\.,0-9]+', lines[j])
                        if price_match:
                            price = price_match.group(0).strip()
                        break
                
                # Additional filters to identify real products
                # Real products usually have: brand name, model, specs, or keyword
                product_keywords = ['laptop', 'notebook', 'asus', 'hp', 'lenovo', 'dell', 'acer',
                                  'intel', 'amd', 'ram', 'ssd', 'hdd', 'inch', 'core', 'ryzen',
                                  'celeron', 'pentium', 'processor', 'windows', 'chromebook',
                                  'gaming', 'ultrabook', 'macbook', 'ipad']
                
                is_product = any(kw in line.lower() for kw in product_keywords)
                
                # Also accept if it has price
                if is_product or (price != "N/A" and len(line) > 20):
                    product = {
                        'name': line[:100],
                        'price': price,
                        'platform': 'Tokopedia'
                    }
                    
                    if product not in products:
                        products.append(product)
        
        # Remove false positives and limit to 20
        real_products = []
        for prod in products:
            # Double-check it's a real product
            name_lower = prod['name'].lower()
            if any(term in name_lower for term in ['laptop', 'notebook', 'computer', 'netbook',
                                                     'chromebook', 'asus', 'hp', 'lenovo', 'dell',
                                                     'acer', 'toshiba', 'intel', 'amd', 'core',
                                                     'ryzen', 'celeron', 'gaming']):
                real_products.append(prod)
        
        products = real_products[:20]
        
        print(f"\n[✓] Successfully extracted {len(products)} real products")
        
        # Display
        print("\n" + "=" * 80)
        print("📦 TOKOPEDIA PRODUCTS")
        print("=" * 80)
        
        for idx, prod in enumerate(products, 1):
            print(f"\n{idx}. {prod['name']}")
            if prod['price'] != 'N/A':
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
            print("\n[✓] Browser closed")

if __name__ == "__main__":
    keyword = sys.argv[1] if len(sys.argv) > 1 else "laptop"
    products = scrape_tokopedia_smart(keyword)
    
    print("\n" + "=" * 80)
    print(f"✅ RESULT: {len(products)} products extracted from Tokopedia")
    print("=" * 80)
    print(json.dumps(products, indent=2, ensure_ascii=False))
