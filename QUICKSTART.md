# 🚀 Quick Start Guide (Panduan Cepat)# 🚀 Darkcrawl Quick Start Guide



Panduan singkat untuk langsung mencoba E-Commerce Scraper.**Get started with Darkcrawl in 5 minutes!**



## 5 Menit Setup ⏱️---



### Step 1: Clone Repository## 1️⃣ Installation

```bash

git clone https://github.com/DarkZagiii/DarkCrawl.git```bash

cd DarkCrawl# Navigate to project

```cd /home/zagii/DarkCrawl



### Step 2: Instalasi Dependencies# Run setup script (automated)

```bashchmod +x setup.sh

bash setup.sh./setup.sh

```

# OR Manual setup

**Atau manual:**python3 -m venv .venv

```bashsource .venv/bin/activate

python -m venv venvpip install -r requirements.txt

source venv/bin/activate```

pip install -r requirements.txt

```---



### Step 3: Test Sekarang!## 2️⃣ Start Web Server



**Option A - Gabungkan Tokopedia + Lazada:**```bash

```bash# Using CLI

python combined_scraper_fixed.py "laptop"python3 -m cli.main serve

```

# OR Direct

Hasil: 40+ produk (20 dari Tokopedia, 20 dari Lazada) ✅python3 -m web.app



**Option B - Hanya Tokopedia:**# Open browser

```bash# http://localhost:5000

python tokopedia_scraper_smart.py "smartphone"```

```

---

**Option C - Hanya Lazada:**

```bash## 3️⃣ Basic Usage

python lazada_scraper_clean.py

```### Via Web Interface (Recommended)



## 30 Menit API Server 🌐1. Open http://localhost:5000

2. Enter URL: `https://example.com`

### Start Server3. Click "Start Scraping"

```bash4. View results

python api_server.py5. Download as JSON/CSV/Excel

```

### Via CLI

Output:

``````bash

Starting Flask API on http://localhost:8000# Scrape single URL

Available endpoints:python3 -m cli.main scrape --query "https://example.com" --output result.json

  GET /api/search?q=keyword

  GET /api/status# Test scraper

```python3 -m cli.main test-scraper --url "https://example.com"



### Test Endpoint# List plugins

python3 -m cli.main list-plugins

**Di terminal baru, buka browser:**

```# Batch scrape

http://localhost:8000/api/search?q=laptoppython3 -m cli.main batch-scrape --file urls.txt --output results.csv

``````



**Atau via terminal:**---

```bash

curl "http://localhost:8000/api/search?q=laptop"## 4️⃣ Create Custom Plugin

```

### Step 1: Create plugin file

**Hasil:** JSON dengan 40 produk + breakdown per platform

```bash

## Contoh Outputtouch plugins/my_plugin.py

```

### Command Line Output

```### Step 2: Write plugin code

================================================================================

🛒 COMBINED E-COMMERCE SCRAPER - FINAL```python

================================================================================from core.base_plugin import BasePlugin



[Tokopedia]  20 productsclass MyPlugin(BasePlugin):

[Lazada]     20 products    def __init__(self):

[Shopee]     0 products (BLOCKED)        super().__init__()

        self.name = "my_plugin"

[TOTAL]      40 products        self.description = "My custom plugin"

        self.supported_sites = ["mysite.com"]

================================================================================    

📦 ALL PRODUCTS    def match(self, url: str) -> bool:

================================================================================        return "mysite.com" in url

    

[TOKOPEDIA - 20 products]    def extract(self, html: str, url: str = None) -> dict:

 1. Laptop HP PROBOOK 440 G6 i5 GEN 8...        # Extract raw data

    💰 Rp3.750.000        return {"url": url, "raw_html": html}

    

[LAZADA - 20 products]    def normalize(self, raw_data: dict) -> dict:

 2. Amoli laptop Silver/pink/Black 14 inch...        # Normalize to standard format

    💰 Rp2.950.000        return {

```            "url": raw_data.get("url"),

            "title": "My Data",

### API Response            "type": "generic"

```json        }

{```

  "status": "success",

  "keyword": "laptop",### Step 3: Test plugin

  "total": 40,

  "products": [```bash

    {python3 -m cli.main list-plugins

      "name": "Laptop HP PROBOOK 440 G6...",# Your plugin should appear in the list

      "price": "Rp3.750.000",```

      "platform": "Tokopedia"

    },---

    ...

  ],## 5️⃣ Database

  "breakdown": {

    "tokopedia": 20,### View database

    "lazada": 20,

    "shopee": 0```bash

  }# Connect to SQLite

}sqlite3 storage/darkcrawl.db

```

# List all tables

## Keyword Examples.tables



Try dengan keyword lain:# View scraped data

SELECT * FROM processed_data LIMIT 5;

```bash

# Electronics# View history

python combined_scraper_fixed.py "smartphone"SELECT * FROM scraping_history LIMIT 5;

python combined_scraper_fixed.py "headphone"

# Exit

# Apparel.quit

python combined_scraper_fixed.py "tas"```

python combined_scraper_fixed.py "sepatu"

### Backup database

# Home

python combined_scraper_fixed.py "lampu"```bash

python combined_scraper_fixed.py "rak"cp storage/darkcrawl.db storage/darkcrawl.db.backup

``````



## Troubleshooting Cepat---



### ❌ Error: "chromedriver not found"## 📚 Key Files

```bash

# Chrome/Chromium sudah terinstall?| File | Purpose |

# Cek:|------|---------|

which chromium| README.md | Full documentation |

# atau| PLUGIN_DEVELOPMENT.md | Plugin creation guide |

which google-chrome| config.yaml | Configuration settings |

```| requirements.txt | Dependencies |

| web/app.py | Web server |

### ❌ Error: "No products found"| core/crawler.py | Core engine |

- Cek koneksi internet| core/base_plugin.py | Plugin template |

- Try keyword yang lebih sederhana

- Tunggu beberapa detik (Tokopedia/Lazada slow)---



### ❌ Error: "ModuleNotFoundError"## 🔧 Configuration

```bash

# Reinstall dependencies### .env file

pip install --force-reinstall -r requirements.txt

``````bash

# Copy template

### ❌ API Port 8000 sudah dipakaicp .env.example .env

```bash

# Edit api_server.py line terakhir:# Edit settings

app.run(host='0.0.0.0', port=8001, debug=False)  # Ubah ke 8001nano .env

``````



## Performa Tips### config.yaml



### Untuk maksimal speed:```yaml

```bashscraper:

# Jalankan hanya 1 platform  timeout: 10

python tokopedia_scraper_smart.py "keyword"  # ~30 detik  delay_min: 1

# vs  delay_max: 3

python combined_scraper_fixed.py "keyword"   # ~60 detik

```web:

  host: 127.0.0.1

### Untuk multiple keywords:  port: 5000

```bash```

# Script loop

for keyword in laptop smartphone tablet; do---

  python combined_scraper_fixed.py "$keyword"

done## 🆘 Troubleshooting

```

### Virtual environment not working

## Next Steps

```bash

1. ✅ Test dengan keyword favorit Anda# Deactivate and reactivate

2. ✅ Check API responsivenessdeactivate

3. ✅ Baca [README.md](./README.md) untuk dokumentasi lengkapsource .venv/bin/activate

4. ✅ Hubungi untuk custom features```



## 📞 Support### Port 5000 already in use



Ada masalah? Cek:```bash

- [README.md](./README.md) → Troubleshooting section# Change port in web/app.py

- [MANIFEST.md](./MANIFEST.md) → Project detailsapp.run(port=5001)

- GitHub Issues → Report bugs

# OR kill process using port 5000

## 🎉 Selamat mencoba!lsof -ti:5000 | xargs kill -9

```

Semoga E-Commerce Scraper berguna untuk project Anda! 🚀

### Database issues

```bash
# Reset database (delete file)
rm storage/darkcrawl.db

# It will be recreated on next run
python3 -m cli.main list-plugins
```

### Import errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 📊 Example Workflows

### Workflow 1: Scrape E-Commerce

```bash
# 1. Test URL
python3 -m cli.main test-scraper --url "https://tokopedia.com/product/xyz"

# 2. Scrape to file
python3 -m cli.main scrape --query "https://tokopedia.com/product/xyz" --output product.json

# 3. Download from web UI
# http://localhost:5000
```

### Workflow 2: Batch Processing

```bash
# 1. Create urls.txt
echo "https://example1.com" > urls.txt
echo "https://example2.com" >> urls.txt

# 2. Batch scrape
python3 -m cli.main batch-scrape --file urls.txt --output batch.csv

# 3. View results
sqlite3 storage/darkcrawl.db "SELECT * FROM processed_data"
```

### Workflow 3: Plugin Development

```bash
# 1. Create plugin
nano plugins/news_plugin.py

# 2. Test it
python3 -m cli.main list-plugins

# 3. Test scraping
python3 -m cli.main test-scraper --url "https://newssite.com"

# 4. Deploy
# Your plugin is now active!
```

---

## 💡 Tips & Tricks

### Export to different formats

```bash
# JSON (best for web)
python3 -m cli.main scrape --query "https://example.com" --output result.json

# CSV (best for spreadsheets)
python3 -m cli.main scrape --query "https://example.com" --output result.csv

# Excel (best for analysis)
python3 -m cli.main scrape --query "https://example.com" --output result.xlsx
```

### Use delays for rate limiting

```bash
# 5 second delay between requests
python3 -m cli.main batch-scrape --file urls.txt --delay 5
```

### Check scraping history

```bash
# View in database
sqlite3 storage/darkcrawl.db "SELECT * FROM scraping_history ORDER BY created_at DESC"

# OR via web API
curl http://localhost:5000/api/history
```

---

## 📖 Full Documentation

For complete documentation, see:

- **README.md** - Full project guide
- **PLUGIN_DEVELOPMENT.md** - Create your own plugins
- **UPDATE_SUMMARY.md** - What's new in v2.0
- **config.yaml** - All configuration options
- **Inline code comments** - Implementation details

---

## ❓ Common Questions

**Q: How do I create a plugin?**  
A: See `PLUGIN_DEVELOPMENT.md` for complete guide

**Q: Can I use with PostgreSQL?**  
A: Yes, update `config.yaml` database settings

**Q: How is data stored?**  
A: Two tables: `raw_scrape` (raw HTML) and `processed_data` (normalized)

**Q: Is it safe to delete the database?**  
A: Yes, it will be recreated. But data will be lost. Backup first!

**Q: How do I contribute?**  
A: Create plugins and submit via GitHub

---

## 🎯 What's Next?

1. ✅ Run setup.sh
2. ✅ Start web server
3. ✅ Access http://localhost:5000
4. ✅ Try scraping a website
5. ✅ Read plugin guide
6. ✅ Create custom plugin
7. ✅ Deploy to production

---

## 📞 Support

- 📖 Check documentation files
- 🐛 Check logs: `logs/darkcrawl.log`
- 💬 Review plugin examples in `core/base_plugin.py`
- 🔍 Debug with `test-scraper` command

---

**Happy Scraping! 🕷️**

**Version:** 2.0.0  
**Last Updated:** November 22, 2025
