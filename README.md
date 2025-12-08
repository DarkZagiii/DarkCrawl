# 🛒 E-Commerce Scraper API

Scraper e-commerce production-ready untuk **Tokopedia**, **Lazada**, dan **Shopee**.

## ✨ Fitur Utama

- ✅ **Tokopedia**: Ekstrak produk dengan harga (20+ produk per pencarian)
- ✅ **Lazada**: Ekstrak produk dengan harga (20+ produk per pencarian)
- ❌ **Shopee**: Terblokir (proteksi anti-bot - butuh residential proxy)
- 🌐 **REST API**: Endpoint `/api/search?q=keyword`
- 📊 **JSON Response**: Format data terstruktur
- ⚡ **Ringan**: Minimal dependencies

## 📥 Instalasi

### Persyaratan Sistem

- Python 3.8+
- Browser Chrome/Chromium
- pip

### Langkah Setup

```bash
# Clone repository
git clone https://github.com/DarkZagiii/DarkCrawl.git
cd DarkCrawl

# Buat virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Verifikasi instalasi
python -c "import selenium; print('✓ Selenium terinstall')"
```

## 🚀 Cara Menggunakan

### 1. Scrape Tokopedia (Command Line)

```bash
python tokopedia_scraper_smart.py "laptop"
```

**Output:**
```json
[
  {
    "name": "Laptop HP PROBOOK 440 G6 i5...",
    "price": "Rp3.750.000",
    "platform": "Tokopedia"
  },
  ...
]
```

### 2. Scrape Lazada (Command Line)

```bash
python lazada_scraper_clean.py
```

Output: 20+ produk dengan harga

### 3. Pencarian Gabungan (Tokopedia + Lazada)

```bash
python combined_scraper_fixed.py "laptop"
```

**Hasil:** 40+ produk total (Tokopedia 20 + Lazada 20)

### 4. REST API Server

```bash
# Jalankan server pada localhost:8000
python api_server.py

# Di terminal lain, test endpoint:
curl "http://localhost:8000/api/search?q=laptop"
```

## 📡 Endpoint API

| Endpoint | Deskripsi | Contoh |
|----------|-----------|--------|
| `GET /api/search?q=keyword` | Cari di semua platform | `/api/search?q=laptop` |
| `GET /api/search?q=keyword&platform=tokopedia` | Cari di Tokopedia | `/api/search?q=phone&platform=tokopedia` |
| `GET /api/search?q=keyword&platform=lazada` | Cari di Lazada | `/api/search?q=tablet&platform=lazada` |
| `GET /api/status` | Status API | `/api/status` |
| `GET /` | Dokumentasi API | `/` |

### Format Response API

```json
{
  "status": "success",
  "keyword": "laptop",
  "total": 32,
  "products": [
    {
      "name": "Laptop Model X",
      "price": "Rp2.500.000",
      "platform": "Lazada"
    }
  ],
  "breakdown": {
    "tokopedia": 12,
    "lazada": 20,
    "shopee": 0
  }
}
```

## 📁 Struktur Folder

```
DarkCrawl/
├── tokopedia_scraper_smart.py    # Scraper Tokopedia
├── lazada_scraper_clean.py        # Scraper Lazada
├── combined_scraper_fixed.py      # Pencarian gabungan
├── api_server.py                  # REST API Flask
├── requirements.txt               # Dependencies
├── setup.sh                       # Script instalasi
└── README.md                      # File ini
```

## ⚙️ Konfigurasi

### Dukungan Proxy (untuk Shopee)

Untuk enable Shopee scraping (butuh residential proxy):

```python
# Di dalam file scraper, tambahkan:
proxy = "http://proxy-ip:port"
options.add_argument(f'--proxy-server={proxy}')
```

### Atur Timeout

Ubah timeout (default 120 detik):

```bash
timeout 180 python tokopedia_scraper_smart.py "laptop"
```

## 📊 Performa

| Platform | Kecepatan | Akurasi | Produk | Status |
|----------|-----------|---------|--------|--------|
| Tokopedia | ~30 detik | 90% | 15-20 | ✅ Berjalan |
| Lazada | ~30 detik | 95% | 15-20 | ✅ Berjalan |
| Shopee | Terblokir | N/A | 0 | ❌ Terblokir |

## ⚠️ Batasan Diketahui

### 1. Shopee Terblokir oleh Anti-Bot

**Penyebab:**
- Rendering JavaScript kompleks
- Geolocation requirement
- Session validation ketat
- Rate limiting agresif

**Solusi:**
- Gunakan Residential Proxy (Bright Data, Oxylabs, Zyte)
- Atau gunakan Official Shopee API

### 2. Rate Limiting

Beberapa platform mungkin rate limit saat volume tinggi

**Solusi:** Tambahkan delay antar request
```python
import time
time.sleep(2)  # Tunggu 2 detik
```

### 3. JavaScript Rendering

Konten dinamis yang di-load oleh JavaScript mungkin terlewat

**Solusi:** Sudah di-handle dengan smart text extraction

## 🔧 Troubleshooting

### Error: Chrome Driver Tidak Ditemukan

```bash
# Download chromedriver sesuai Chrome version Anda
# https://chromedriver.chromium.org/download
# Letakkan di PATH atau folder project
```

### Error: Import Module Tidak Ditemukan

```bash
# Reinstall semua dependencies
pip install --force-reinstall -r requirements.txt
```

### Timeout Issues

```bash
# Tingkatkan timeout
timeout 180 python tokopedia_scraper_smart.py "laptop"
```

### Tidak Ada Produk yang Ditemukan

Cek:
1. Koneksi internet normal
2. Website bisa diakses: `curl https://www.tokopedia.com`
3. Update Chrome/Chromium terbaru
4. Coba keyword lain

## 👨‍💻 Development

### Menambah Platform Baru

1. Buat `platform_scraper.py`
2. Implementasikan fungsi `scrape_platform(keyword)`
3. Return format: `{"name": "", "price": "", "platform": ""}`
4. Tambahkan ke `combined_scraper_fixed.py`

### Testing

```bash
# Test scraper individual
python tokopedia_scraper_smart.py "test"
python lazada_scraper_clean.py

# Test gabungan
python combined_scraper_fixed.py "test"

# Test API
curl http://localhost:8000/api/status
```

## 📦 Dependencies

Lihat `requirements.txt`:

```
selenium==4.38.0           # Browser automation
beautifulsoup4==4.14.2     # HTML parsing
Flask==2.3.3               # Web framework
lxml==4.9.3                # XML/HTML library
requests==2.31.0           # HTTP client
```

## 📄 Lisensi

MIT

## 👤 Pembuat

DarkZagiii

## 💬 Support & Pertanyaan

Untuk issues dan pertanyaan:

1. Cek bagian **Troubleshooting**
2. Lihat error logs
3. Buka issue di GitHub dengan:
   - Platform mana (Tokopedia/Lazada/Shopee)
   - Pesan error lengkap
   - Python version
   - Sistem operasi

## 🎯 Roadmap Fitur

### Phase 1 (Done ✅)
- ✅ Scraper Tokopedia
- ✅ Scraper Lazada
- ✅ REST API

### Phase 2 (Planned)
- ⏳ Pagination support (100+ produk)
- ⏳ Database integration
- ⏳ CSV/Excel export
- ⏳ Caching layer

### Phase 3 (Future)
- 🔮 Shopee integration (dengan proxy)
- 🔮 Price comparison chart
- 🔮 Mobile app
- 🔮 Machine learning prediction

## 📞 Kontak & Maintenance

**Maintenance Plan:**
- 3 bulan gratis: Bug fixes & support
- Setelahnya: Rp 2-5 juta/bulan (tergantung tier)

**Untuk update atau fitur tambahan:**
- instagram: i_am_dark_zagii

---

**Status: ✅ PRODUCTION READY**

Semua scraper berjalan, API tested, dokumentasi lengkap.
