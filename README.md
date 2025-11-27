# E-Commerce Scraper API# � **DarkCrawl – Universal Web Scraper Framework**



Scraper e-commerce production-ready untuk Tokopedia, Lazada, dan Shopee.> **Status: ✅ READY FOR TESTING** | Version 2.0 | Selenium Integration Complete



## Features ✨## 📖 Overview



- ✅ **Tokopedia**: Extract products dengan harga (20+ produk per search)**DarkCrawl** adalah *universal, modular, dan pluggable web-scraping framework* yang memungkinkan scraping dari berbagai website (e-commerce, news, forum, dll.) menggunakan antarmuka web yang mudah digunakan.

- ✅ **Lazada**: Extract products dengan harga (20+ produk per search)

- ❌ **Shopee**: Blocked (anti-bot protection - butuh residential proxy)Framework ini memiliki arsitektur **plugin-based** dengan dukungan:

- 🌐 **REST API**: `/api/search?q=keyword` endpoint- ✅ **Selenium WebDriver** untuk JavaScript-heavy sites (Shopee, Tokopedia, Lazada)

- 📊 **JSON Response**: Structured product data- ✅ **Requests library** untuk fallback scraping yang cepat

- ⚡ **Lightweight**: Minimal dependencies- ✅ **Multi-strategy extraction** untuk hasil yang akurat

- ✅ **Web interface** tanpa perlu command line

## Installation- ✅ **REST API** untuk integrasi programmatic

- ✅ **SQLite database** untuk penyimpanan

### Requirements

- Python 3.8+### Arsitektur 3-Tier

- Chrome/Chromium browser

- pip```

Raw Data Collection → Data Normalization → Storage & Export

### Setup```



```bash---

# Clone repository

git clone https://github.com/DarkZagiii/DarkCrawl.git## 🎯 Fitur Utama

cd DarkCrawl

### 1️⃣ **Smart Scraping**

# Create virtual environment- ✅ Auto-detect platform (Shopee, Tokopedia, Lazada)

python -m venv venv- ✅ Dual-method (requests + Selenium fallback)

source venv/bin/activate  # Linux/Mac- ✅ Intelligent routing to appropriate scraper

# or- ✅ Error handling dengan graceful degradation

venv\Scripts\activate  # Windows

### 2️⃣ **JavaScript Support**

# Install dependencies- ✅ Selenium WebDriver integration

pip install -r requirements.txt- ✅ 30-40 second render time (but accurate)

- ✅ Wait strategies untuk dynamic content

# Verify installation- ✅ Automated browser management

python -c "import selenium; print('✓ Selenium installed')"

```### 3️⃣ **Advanced Parsing**

- ✅ 3-tier extraction strategies

## Usage- ✅ Multiple CSS selectors fallback

- ✅ Aggressive div scanning for robustness

### 1. Command Line - Tokopedia- ✅ Deduplication dan data cleaning



```bash### 4️⃣ **Web Interface**

python tokopedia_scraper_smart.py "laptop"- ✅ Modern, user-friendly UI

```- ✅ Real-time scraping progress

- ✅ Results display dengan formatting

**Output:**- ✅ CSV/JSON export

```json

[### 5️⃣ **API Endpoints**

  {- ✅ POST /api/scrape

    "name": "HIGH QUALITY !! Laptop HP PROBOOK 440 G6...",- ✅ GET /api/results

    "price": "Rp3.750.000",- ✅ JSON response format

    "platform": "Tokopedia"- ✅ Programmatic access

  },* User hanya input URL → engine jalan otomatis

  ...

]### **2. Plugin-Based Architecture**

```

Contoh plugin:

### 2. Command Line - Lazada

* `plugin_ecommerce_tokopedia.py`

```bash* `plugin_shopee.py`

python lazada_scraper_clean.py* `plugin_instagram.py`

```* `plugin_youtube.py`



### 3. Combined SearchSetiap plugin memiliki fungsi:



```bash* `scrape_raw(url)`

python combined_scraper_fixed.py "laptop"* `normalize(raw_data)`

```* `save_to_db(clean_data)`



Returns **30+ products** (Tokopedia + Lazada combined)### **3. Database System**



### 4. REST API ServerMenggunakan dua tipe penyimpanan:



```bash#### a) `raw_scrape` table

# Start server on localhost:8000

python api_server.pyUntuk menyimpan hasil mentah:



# In another terminal, test endpoint:* url

curl "http://localhost:8000/api/search?q=laptop"* scraped_at

```* raw_json

* plugin

**API Endpoints:*** status



| Endpoint | Description | Example |#### b) Processed tables

|----------|-------------|---------|

| `GET /api/search?q=keyword` | Search all platforms | `/api/search?q=laptop` |Tergantung kategori:

| `GET /api/search?q=keyword&platform=tokopedia` | Tokopedia only | `/api/search?q=phone&platform=tokopedia` |

| `GET /api/search?q=keyword&platform=lazada` | Lazada only | `/api/search?q=tablet&platform=lazada` |* `ecommerce_products`

| `GET /api/status` | API status | `/api/status` |* `instagram_posts`

| `GET /` | API documentation | `/` |* `youtube_videos`



**API Response Format:**### **4. Data Normalization Layer**



```jsonMengubah raw HTML/JSON → data Python dict konsisten.

{

  "status": "success",Contoh output normalized untuk e-commerce:

  "keyword": "laptop",

  "total": 32,```json

  "products": [{

    {  "product_id": "xyz123",

      "name": "Laptop Model X",  "name": "Headphone Gaming",

      "price": "Rp2.500.000",  "price": 180000,

      "platform": "Lazada"  "currency": "IDR",

    }  "store_name": "Toko Audio",

  ],  "total_sold": 356,

  "breakdown": {  "rating": 4.8,

    "tokopedia": 12,  "url": "https://tokopedia.com/...",

    "lazada": 20,  "image_url": "https://..."

    "shopee": 0}

  }```

}

```### **5. Web Interface**



## File StructureFitur UI:



```* Input URL

DarkCrawl/* Pilih plugin (atau autodetect)

├── tokopedia_scraper_smart.py    # Tokopedia scraper* History scraping

├── lazada_scraper_clean.py        # Lazada scraper* Tampilkan hasil processed

├── combined_scraper_fixed.py      # Combined search* Download CSV / JSON

├── api_server.py                  # Flask REST API* Log error debugging

├── requirements.txt               # Dependencies

└── README.md                      # This file### **6. Export System**

```

User bisa download:

## Configuration

* CSV

### Proxy Support (Shopee)* JSON

* (opsional) Excel

To enable Shopee scraping (requires residential proxy):

---

```python

# In scraper file, add:# **📐 Project Architecture Overview**

proxy = "http://proxy-ip:port"

options.add_argument(f'--proxy-server={proxy}')```

```[Web UI]

   |

### Timeout Settings   V

[Core API Router] --- chooses plugin ---> [Plugin A/B/C]

Adjust timeout (default 120s):   |

   V

```bash[Scraping Engine] -> raw_data -> [raw_scrape DB]

timeout 180 python tokopedia_scraper_smart.py "laptop"   |

```Normalization

   |

## Performance   V

[Processed DB Tables]

| Platform | Speed | Accuracy | Products | Status |   |

|----------|-------|----------|----------|--------|   V

| Tokopedia | ~30s | 90% | 15-20 | ✅ Working |[Export / Dashboard / Analytics]

| Lazada | ~30s | 95% | 15-20 | ✅ Working |```

| Shopee | Blocked | N/A | 0 | ❌ Blocked |

---

## Known Limitations

# **⚙️ Technology Stack**

1. **Shopee**: Blocked by anti-bot protection

   - Solution: Use residential proxy service* **Backend**: Python (FastAPI / Flask)

   - Recommended: Bright Data, Oxylabs, Zyte* **Scraping**: Requests, Playwright (optional)

* **Database**: SQLite (local), PostgreSQL/MySQL (server)

2. **Rate Limiting**: Some platforms may rate limit* **Frontend**: HTML/Tailwind/React (opsional simple)

   - Solution: Add delays between requests* **ORM**: SQLAlchemy atau raw-SQL

   - Use: `time.sleep(2)` between requests

---

3. **JavaScript Rendering**: May miss dynamic content

   - Lazada uses JS rendering for products# **📁 File Structure (Disarankan)**

   - Fixed: Smart text-based extraction

```

## Troubleshootingdarkcrawl/

│

### Chrome Driver Not Found├── core/

│   ├── engine.py

```bash│   ├── router.py

# Download chromedriver matching your Chrome version│   ├── database.py

# Place in PATH or project directory│   └── normalize.py

wget https://chromedriver.chromium.org/download│

```├── plugins/

│   ├── ecommerce_tokopedia.py

### Import Errors│   ├── ecommerce_shopee.py

│   ├── instagram.py

```bash│   └── youtube.py

# Reinstall all dependencies│

pip install --force-reinstall -r requirements.txt├── web/

```│   ├── app.py

│   └── templates/

### Timeout Issues│

├── storage/

```bash│   └── darkcrawl.db

# Increase timeout│

timeout 180 python tokopedia_scraper_smart.py "laptop"└── README.md

``````



### No Products Found---



1. Check internet connection# **🤖 Why AI Concept Removed (Lightweight Mode)?**

2. Verify site is accessible: `curl https://www.tokopedia.com`

3. Update selectors if site structure changedVersi baru *tidak menggunakan AI model berat* di lokal.

4. Check Chrome version compatibilitySemua pemrosesan dilakukan melalui:



## Development* parsing HTML

* regex

### Adding New Platform* struktur JSON



1. Create `platform_scraper.py`Tidak membebani laptop.

2. Implement `scrape_platform(keyword)` function

3. Return JSON: `{"name": "", "price": "", "platform": ""}`---

4. Add to `combined_scraper_fixed.py`

# **📌 What Darkcrawl Does (Simple Version)**

### Testing

**User input link → Plugin scrape → Normalize → Save to DB → UI menampilkan data bersih.**

```bash

# Test individual scrapersTidak lebih, tidak kurang.

python tokopedia_scraper_smart.py "test"Ringan. Fokus. Jelas.

python lazada_scraper_clean.py

---

# Test combined

python combined_scraper_fixed.py "test"# **🏁 Kesimpulan Singkat**



# Test API**Darkcrawl adalah framework scraping modular** yang memakai database agar hasil bisa diproses rapi dan tampil di web interface. Dirancang supaya berkembang menjadi sistem besar (mirip mini-Octoparse tapi versi open-source).

curl http://localhost:8000/api/status

```---

## Dependencies

See `requirements.txt`:

```
selenium==4.38.0
beautifulsoup4==4.14.2
Flask==2.3.3
lxml==4.9.3
requests==2.31.0
```

## License

MIT

## Author

DarkZagiii

## Support

For issues and questions:
1. Check Troubleshooting section
2. Review error logs
3. Open GitHub issue with:
   - Platform (Tokopedia/Lazada/Shopee)
   - Error message
   - Python version
   - OS
