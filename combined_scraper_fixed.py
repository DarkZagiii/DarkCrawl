#!/usr/bin/env python3
"""
Combined E-commerce Scraper - FIXED
Tokopedia + Lazada (Shopee blocked by anti-bot)
"""
import subprocess
import json
import sys
import re

def scrape_tokopedia():
    """Run Tokopedia scraper and extract results"""
    try:
        print("\n[*] Running Tokopedia scraper...")
        result = subprocess.run(
            [sys.executable, "tokopedia_scraper_smart.py", "laptop"],
            cwd="/home/zagii/DarkCrawl",
            capture_output=True,
            text=True,
            timeout=120
        )
        
        # Look for JSON in output
        lines = result.stdout.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith('['):
                # Found JSON array
                json_str = '\n'.join(lines[i:])
                try:
                    products = json.loads(json_str)
                    print(f"[✓] Tokopedia found {len(products)} products")
                    return products
                except json.JSONDecodeError:
                    pass
        
        return []
        
    except subprocess.TimeoutExpired:
        print("[✗] Tokopedia scraper timed out")
        return []
    except Exception as e:
        print(f"[✗] Error scraping Tokopedia: {e}")
        return []

def scrape_lazada(keyword="laptop"):
    """Run Lazada scraper and extract results"""
    try:
        print(f"\n[*] Running Lazada scraper for '{keyword}'...")
        result = subprocess.run(
            [sys.executable, "lazada_scraper_clean.py"],
            cwd="/home/zagii/DarkCrawl",
            capture_output=True,
            text=True,
            timeout=120
        )
        
        # Look for JSON in output
        lines = result.stdout.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith('['):
                # Found JSON array
                json_str = '\n'.join(lines[i:])
                try:
                    products = json.loads(json_str)
                    print(f"[✓] Lazada found {len(products)} products")
                    return products
                except json.JSONDecodeError:
                    pass
        
        return []
        
    except subprocess.TimeoutExpired:
        print("[✗] Lazada scraper timed out")
        return []
    except Exception as e:
        print(f"[✗] Error scraping Lazada: {e}")
        return []

def main():
    keyword = sys.argv[1] if len(sys.argv) > 1 else "laptop"
    
    print("=" * 80)
    print("🛒 COMBINED E-COMMERCE SCRAPER - FINAL")
    print("=" * 80)
    print(f"\n[*] Searching for: '{keyword}'")
    print("[*] Platforms: Tokopedia + Lazada (Shopee blocked by anti-bot)")
    
    # Run scrapers
    tokopedia_products = scrape_tokopedia()
    lazada_products = scrape_lazada(keyword)
    
    # Combine results
    combined = {
        'timestamp': __import__('datetime').datetime.now().isoformat(),
        'source': 'Combined E-commerce Scraper',
        'keyword': keyword,
        'platforms': {
            'tokopedia': {
                'count': len(tokopedia_products),
                'products': tokopedia_products
            },
            'lazada': {
                'count': len(lazada_products),
                'products': lazada_products
            },
            'shopee': {
                'count': 0,
                'status': 'BLOCKED - Anti-bot protection requires residential proxy',
                'products': []
            }
        },
        'total': len(tokopedia_products) + len(lazada_products)
    }
    
    # Display summary
    print("\n" + "=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print(f"\n[Tokopedia]  {combined['platforms']['tokopedia']['count']} products")
    print(f"[Lazada]     {combined['platforms']['lazada']['count']} products")
    print(f"[Shopee]     {combined['platforms']['shopee']['count']} products (BLOCKED)")
    print(f"\n[TOTAL]      {combined['total']} products")
    
    # Display products
    print("\n" + "=" * 80)
    print("📦 ALL PRODUCTS")
    print("=" * 80)
    
    product_num = 1
    
    if tokopedia_products:
        print(f"\n[TOKOPEDIA - {len(tokopedia_products)} products]")
        for prod in tokopedia_products[:10]:
            name = prod.get('name', 'N/A')
            if len(name) > 80:
                name = name[:77] + "..."
            print(f"{product_num:2d}. {name}")
            price = prod.get('price', 'N/A')
            if price != 'N/A':
                print(f"    💰 {price}")
            product_num += 1
    
    if lazada_products:
        print(f"\n[LAZADA - {len(lazada_products)} products]")
        for prod in lazada_products[:10]:
            name = prod.get('name', 'N/A')
            if len(name) > 80:
                name = name[:77] + "..."
            print(f"{product_num:2d}. {name}")
            price = prod.get('price', 'N/A')
            if price != 'N/A':
                print(f"    💰 {price}")
            product_num += 1
    
    # Output JSON
    print("\n" + "=" * 80)
    print("✅ COMPLETE RESULT (JSON)")
    print("=" * 80)
    print(json.dumps(combined, indent=2, ensure_ascii=False))
    
    return combined

if __name__ == "__main__":
    main()
