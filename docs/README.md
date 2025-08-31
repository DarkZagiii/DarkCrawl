# AI Scraper Framework

Framework modular untuk scraping web berbasis CLI dengan dukungan plugin dan LLM.

## Fitur Utama
- Scrape berbagai jenis situs (berita, produk, forum, dll)
- Deteksi konteks halaman dengan LLM (OpenChat, DeepSeek, Ollama, dsb)
- Sistem plugin Python class
- Operasi via prompt natural language
- Ekspor ke CSV, JSON, Markdown
- Ringkasan artikel otomatis

## Struktur Folder
```
ai-scraper-framework/
├── core/
├── plugins/
├── cli/
├── utils/
├── data/
├── docs/
├── requirements.txt
└── config.yaml
```

## Instalasi
```
pip install -r requirements.txt
```

## Contoh Penggunaan
```
scrape "cari harga laptop Asus di toko lokal Indonesia" --output laptop.csv
# 1. Scraping produk di tokopedia
python -m cli.main scrape --query "https://www.tokopedia.com/search?st=product&q=iphone%2015" --selenium --output tokopedia_iphone.csv

# 2. Scraping produk di Shopee  
python -m cli.main scrape --query "https://shopee.co.id/search?keyword=samsung%20galaxy" --selenium --delay 3 --output shopee_samsung.csv

# 3. Batch scraping e-commerce
echo "https://tokopedia.com/p/handphone-tablet" > urls_ecommerce.txt
echo "https://shopee.co.id/Handphone-cat.40" >> urls_ecommerce.txt
python -m cli.main batch-scrape --file urls_ecommerce.txt --selenium --output semua_ecommerce.csv
[hapus link di contoh dan tempel link anda untuk melakukan scrape, dan ganti nama output sesuai dengan pilihan anda contoh -- output data_web A.csv atau formater lainya]

```

## Kontribusi
Buat plugin baru di folder `plugins/` mengikuti template yang ada.
