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
```

## Kontribusi
Buat plugin baru di folder `plugins/` mengikuti template yang ada.
