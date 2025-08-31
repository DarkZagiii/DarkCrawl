from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import time
from datetime import datetime
import pandas as pd
from core.universal_scraper import UniversalScraper
from utils.formatter import Formatter

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULTS_FOLDER'] = 'results'

# Buat folder jika belum ada
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

class DataProcessor:
    @staticmethod
    def process_raw_data(raw_data):
        """Olah data mentah menjadi terstruktur"""
        processed = {
            'metadata': {
                'total_items': len(raw_data),
                'processed_at': datetime.now().isoformat(),
                'platform': 'universal'
            },
            'products': [],
            'categories': {},
            'statistics': {
                'total_images': 0,
                'total_links': 0,
                'total_words': 0,
                'price_range': {'min': None, 'max': None}
            }
        }
        
        for item in raw_data:
            # Ekstrak produk dari data
            product = {
                'id': str(hash(item.get('url', '')))[:8],
                'title': item.get('title', 'No Title'),
                'description': item.get('description', '')[:200] + '...',
                'content': item.get('content', '')[:500] + '...',
                'price': DataProcessor.extract_price(item),
                'images': item.get('images', [])[:5],
                'links': item.get('links', [])[:10],
                'category': DataProcessor.categorize_content(item),
                'metadata': {
                    'url': item.get('url', ''),
                    'extracted_at': item.get('extracted_at', ''),
                    'word_count': len(item.get('content', '').split()),
                    'image_count': len(item.get('images', [])),
                    'link_count': len(item.get('links', []))
                }
            }
            processed['products'].append(product)
            
            # Update statistik
            processed['statistics']['total_images'] += len(item.get('images', []))
            processed['statistics']['total_links'] += len(item.get('links', []))
            processed['statistics']['total_words'] += len(item.get('content', '').split())
            
            # Kategorikan konten
            category = product['category']
            if category not in processed['categories']:
                processed['categories'][category] = 0
            processed['categories'][category] += 1
        
        return processed
    
    @staticmethod
    def extract_price(item):
        """Ekstrak harga dari konten"""
        content = item.get('content', '') + ' ' + item.get('description', '')
        import re
        
        # Pattern untuk harga Rupiah
        price_patterns = [
            r'Rp[\d.,]+',
            r'IDR[\d.,]+',
            r'[\d.,]+\s*ribu',
            r'[\d.,]+\s*juta'
        ]
        
        for pattern in price_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                return matches[0]
        
        return 'Price not found'
    
    @staticmethod
    def categorize_content(item):
        """Kategorikan konten berdasarkan konten"""
        content = item.get('content', '').lower()
        url = item.get('url', '').lower()
        
        if any(keyword in content or keyword in url for keyword in ['laptop', 'komputer', 'pc']):
            return 'Elektronik'
        elif any(keyword in content or keyword in url for keyword in ['handphone', 'smartphone', 'hp']):
            return 'Handphone'
        elif any(keyword in content or keyword in url for keyword in ['baju', 'pakaian', 'fashion']):
            return 'Fashion'
        elif any(keyword in content or keyword in url for keyword in ['makanan', 'minuman', 'food']):
            return 'Makanan'
        else:
            return 'Lainnya'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        data = request.json
        url = data.get('url')
        use_selenium = data.get('use_selenium', False)
        delay = data.get('delay', 2)
        output_format = data.get('format', 'json')
        
        if not url:
            return jsonify({'error': 'URL tidak boleh kosong'}), 400
        
        # Scraping dengan UniversalScraper
        with UniversalScraper(use_selenium=use_selenium) as scraper:
            html = scraper.fetch_page(url)
            if not html:
                return jsonify({'error': 'Gagal mengambil data dari URL'}), 400
            
            raw_data = [scraper.extract_universal_data(html, url)]
            
            # Olah data menjadi terstruktur
            processed_data = DataProcessor.process_raw_data(raw_data)
            
            # Simpan hasil
            filename = f"scraped_{int(time.time())}.{output_format}"
            filepath = os.path.join(app.config['RESULTS_FOLDER'], filename)
            
            if output_format == 'json':
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(processed_data, f, indent=2, ensure_ascii=False)
            elif output_format == 'csv':
                df = pd.DataFrame(processed_data['products'])
                df.to_csv(filepath, index=False, encoding='utf-8')
            elif output_format == 'xlsx':
                df = pd.DataFrame(processed_data['products'])
                df.to_excel(filepath, index=False)
            
            return jsonify({
                'success': True,
                'data': processed_data,
                'download_url': f'/download/{filename}',
                'summary': {
                    'total_products': len(processed_data['products']),
                    'categories': processed_data['categories'],
                    'statistics': processed_data['statistics']
                }
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download(filename):
    filepath = os.path.join(app.config['RESULTS_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({'error': 'File tidak ditemukan'}), 404

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """API untuk analisis data yang sudah discrape"""
    try:
        data = request.json
        raw_data = data.get('data', [])
        
        processed = DataProcessor.process_raw_data(raw_data)
        
        return jsonify({
            'success': True,
            'analysis': {
                'total_items': len(processed['products']),
                'categories': processed['categories'],
                'price_analysis': processed['statistics'],
                'insights': {
                    'most_common_category': max(processed['categories'].items(), key=lambda x: x[1])[0] if processed['categories'] else None,
                    'average_price': 'Rp' + str(sum([float(p['price'].replace('Rp', '').replace('.', '').replace(',', '')) for p in processed['products'] if p['price'] != 'Price not found']) / len([p for p in processed['products'] if p['price'] != 'Price not found'])) if any(p['price'] != 'Price not found' for p in processed['products']) else 'Tidak ada harga'
                }
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
