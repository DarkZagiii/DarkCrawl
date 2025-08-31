# Universal Web Scraper

Scraper universal yang dapat menangani berbagai jenis website dengan dukungan JavaScript rendering dan ekstraksi data komprehensif.

## Fitur Utama

- ✅ **Universal Scraping**: Bisa digunakan untuk semua jenis website
- ✅ **JavaScript Support**: Menggunakan Selenium untuk website berbasis JavaScript
- ✅ **Multi-format Output**: CSV, JSON, Markdown, Excel
- ✅ **Batch Processing**: Scraping multiple URLs sekaligus
- ✅ **Comprehensive Data Extraction**: 
  - Judul, deskripsi, konten
  - Gambar dan link
  - Meta tags dan structured data
  - Tabel, list, form
  - Social media links
  - Contact information
- ✅ **Anti-bot Measures**: User-agent rotation, delays
- ✅ **Error Handling**: Robust error handling dan retry mechanism

## Instalasi

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install ChromeDriver (untuk Selenium)
```bash
# Otomatis dengan webdriver-manager
# Atau manual download dari https://chromedriver.chromium.org/
```

## Cara Penggunaan

### 1. Scraping Single URL
```bash
# Basic scraping
python -m cli.main scrape --query "https://example.com" --output result.csv

# Dengan Selenium untuk JavaScript-heavy sites
python -m cli.main scrape --query "https://example.com" --selenium --delay 3

# Output JSON
python -m cli.main scrape --query "https://example.com" --output result.json
```

### 2. Batch Scraping
```bash
# Buat file urls.txt dengan daftar URL
echo "https://example1.com" > urls.txt
echo "https://example2.com" >> urls.txt

# Jalankan batch scraping
python -m cli.main batch-scrape --file urls.txt --output batch_results.csv --delay 2
```

### 3. Testing
```bash
# Test scraper pada satu URL
python -m cli.main test-scraper --url "https://example.com"
```

## Struktur Data Output

Setiap item hasil scraping berisi:

```json
{
  "url": "https://example.com",
  "title": "Judul Halaman",
  "description": "Deskripsi halaman dari meta tags",
  "content": "Konten utama halaman",
  "text_content": "Semua teks dari halaman",
  "images": [
    {
      "url": "https://example.com/image.jpg",
      "alt": "Alt text",
      "title": "Image title"
    }
  ],
  "links": [
    {
      "url": "https://example.com/link",
      "text": "Link text",
      "title": "Link title"
    }
  ],
  "meta_tags": {
    "description": "Meta description",
    "keywords": "keyword1, keyword2"
  },
  "structured_data": {
    "json_ld": [...],
    "open_graph": {...},
    "twitter_card": {...}
  },
  "headings": {
    "h1": ["Heading 1"],
    "h2": ["Heading 2"]
  },
  "tables": [...],
  "forms": [...],
  "social_media": {
    "facebook": [...],
    "twitter": [...]
  },
  "contact_info": {
    "emails": [...],
    "phones": [...]
  },
  "extracted_at": "2024-01-01 12:00:00"
}
```

## Opsi Command Line

### Perintah `scrape`
- `--query, -q`: URL atau prompt untuk scraping
- `--output`: Nama file output (default: output.csv)
- `--plugin`: Nama plugin (opsional)
- `--selenium, -s`: Gunakan Selenium untuk JavaScript
- `--delay, -d`: Delay antar request (detik)

### Perintah `batch-scrape`
- `--file, -f`: File berisi daftar URL
- `--output`: Nama file output
- `--selenium, -s`: Gunakan Selenium
- `--delay, -d`: Delay antar request

### Perintah `test-scraper`
- `--url, -u`: URL untuk testing

## Contoh Penggunaan

### 1. Scraping E-commerce
```bash
python -m cli.main scrape --query "https://www.tokopedia.com/p/handphone-tablet" --selenium --output tokopedia.csv
```

### 2. Scraping News Website
```bash
python -m cli.main scrape --query "https://news.detik.com" --output news.json
```

### 3. Scraping Forum
```bash
python -m cli.main scrape --query "https://kaskus.co.id" --selenium --delay 5 --output forum_data.csv
```

## Troubleshooting

### Error: ChromeDriver not found
```bash
# Install ChromeDriver otomatis
pip install webdriver-manager
```

### Error: Permission denied
```bash
# Pada Linux/Mac
chmod +x chromedriver
```

### Error: Timeout
```bash
# Tambahkan delay lebih lama
python -m cli.main scrape --query "https://example.com" --delay 5 --timeout 30
```

## Tips

1. **Gunakan Selenium** untuk website dengan konten dinamis
2. **Tambahkan delay** untuk menghindari rate limiting
3. **Gunakan batch processing** untuk scraping banyak URL
4. **Test terlebih dahulu** dengan perintah `test-scraper`
5. **Gunakan output JSON** untuk data yang kompleks

## Pengembangan Lanjutan

Untuk menambahkan plugin khusus, buat file di folder `plugins/` dengan format:

```python
from core.base_plugin import BasePlugin

class CustomPlugin(BasePlugin):
    def match(self, url):
        return "custom-site.com" in url
        
    def extract(self, html, url=None):
        # Custom extraction logic
        return data
```

## Lisensi

MIT License - Bebas digunakan untuk proyek personal dan komersial.


## text sementara
gunakan  perintah di bawah untuk melakukan test web di local host 
'''bash
cd