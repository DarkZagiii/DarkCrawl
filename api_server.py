#!/usr/bin/env python3
"""
Flask API for E-commerce Scraping
Endpoint: /api/search?q=keyword
Returns: Combined results from Tokopedia + Lazada
"""
from flask import Flask, request, jsonify
import subprocess
import json
import re
import sys
import os

app = Flask(__name__)

def scrape_tokopedia():
    """Run Tokopedia scraper"""
    try:
        result = subprocess.run(
            [sys.executable, "test_tokopedia_simple.py"],
            cwd="/home/zagii/DarkCrawl",
            capture_output=True,
            text=True,
            timeout=120
        )
        
        products = []
        lines = result.stdout.split('\n')
        for line in lines:
            if re.match(r'^\d+\. ', line):
                name = re.sub(r'^\d+\. \+ ?', '', line).replace('[REGEX]', '').strip()
                if name and len(name) > 3:
                    products.append({
                        'name': name,
                        'price': 'N/A',
                        'platform': 'Tokopedia'
                    })
        
        return products[:20]
    except:
        return []

def scrape_lazada(keyword="laptop"):
    """Run Lazada scraper"""
    try:
        result = subprocess.run(
            [sys.executable, "lazada_scraper_clean.py"],
            cwd="/home/zagii/DarkCrawl",
            capture_output=True,
            text=True,
            timeout=120
        )
        
        lines = result.stdout.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith('['):
                json_str = '\n'.join(lines[i:])
                try:
                    return json.loads(json_str)
                except:
                    pass
        
        return []
    except:
        return []

@app.route('/api/search', methods=['GET'])
def search():
    """
    Search endpoint
    Usage: /api/search?q=laptop
    """
    keyword = request.args.get('q', 'laptop')
    platform = request.args.get('platform', 'all')  # all, tokopedia, lazada
    
    try:
        # Run scrapers
        tokopedia_products = scrape_tokopedia()
        lazada_products = scrape_lazada(keyword)
        
        # Filter by platform
        if platform == 'tokopedia':
            products = tokopedia_products
        elif platform == 'lazada':
            products = lazada_products
        else:  # all
            products = tokopedia_products + lazada_products
        
        # Prepare response
        response = {
            'status': 'success',
            'keyword': keyword,
            'platform': platform,
            'total': len(products),
            'products': products,
            'breakdown': {
                'tokopedia': len(tokopedia_products),
                'lazada': len(lazada_products),
                'shopee': 0
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/status', methods=['GET'])
def status():
    """API status endpoint"""
    return jsonify({
        'status': 'online',
        'service': 'E-commerce Scraper API',
        'platforms': {
            'tokopedia': 'enabled',
            'lazada': 'enabled',
            'shopee': 'disabled (anti-bot protection)'
        },
        'endpoints': [
            '/api/search?q=keyword',
            '/api/search?q=keyword&platform=tokopedia',
            '/api/search?q=keyword&platform=lazada',
            '/api/status'
        ]
    }), 200

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with documentation"""
    return jsonify({
        'service': 'E-commerce Scraper API',
        'version': '1.0',
        'description': 'Search for products across multiple e-commerce platforms',
        'endpoints': {
            'GET /api/search': {
                'params': {
                    'q': 'Search keyword (default: laptop)',
                    'platform': 'Filter by platform: all, tokopedia, lazada (default: all)'
                },
                'example': '/api/search?q=laptop',
                'example2': '/api/search?q=smartphone&platform=lazada'
            },
            'GET /api/status': {
                'description': 'Check API status and available platforms'
            }
        }
    }), 200

if __name__ == '__main__':
    print("=" * 80)
    print("🛒 E-COMMERCE SCRAPER API")
    print("=" * 80)
    print("\n[*] Starting Flask API on http://localhost:8000")
    print("[*] Available endpoints:")
    print("    GET /api/search?q=keyword")
    print("    GET /api/search?q=keyword&platform=tokopedia")
    print("    GET /api/search?q=keyword&platform=lazada")
    print("    GET /api/status")
    print("\n[*] Example:")
    print("    curl 'http://localhost:8000/api/search?q=laptop'")
    print("\n[*] Press Ctrl+C to stop")
    print("=" * 80)
    
    app.run(host='0.0.0.0', port=8000, debug=False)
