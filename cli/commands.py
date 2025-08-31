"""
commands.py
Definisi perintah CLI yang diperbarui untuk universal web scraping
"""

import typer
import os
import re
import time
import json
from typing import List, Dict, Any

def scrape(
    query: str = typer.Option(..., "--query", "-q", help="URL atau prompt untuk scraping"),
    output: str = typer.Option("output.csv", help="Nama file output"),
    plugin: str = typer.Option(None, help="Nama plugin (opsional)"),
    selenium: bool = typer.Option(False, "--selenium", "-s", help="Gunakan Selenium untuk JavaScript-heavy sites"),
    delay: int = typer.Option(2, "--delay", "-d", help="Delay antar request (detik)")
):
    """Perintah scraping universal untuk semua jenis website"""
    
    from core.universal_scraper import UniversalScraper
    from core.plugin_loader import PluginLoader
    from core.summarizer import Summarizer
    from utils.formatter import Formatter
    
    typer.echo(f"[CLI] Mulai scraping: {query}")
    typer.echo(f"Output: {output} | Plugin: {plugin} | Selenium: {selenium}")
    
    # Validasi dan ekstrak URL
    url_pattern = re.compile(r'https?://[^\s<>]+')
    urls = url_pattern.findall(query)
    
    if not urls:
        if query.startswith('http'):
            urls = [query]
        else:
            typer.echo("[ERROR] Tidak ada URL valid ditemukan")
            raise typer.Exit(1)
    
    # Setup scraper
    with UniversalScraper(use_selenium=selenium) as scraper:
        all_results = []
        
        for idx, url in enumerate(urls):
            typer.echo(f"[{idx+1}/{len(urls)}] Memproses: {url}")
            
            html = scraper.fetch_page(url)
            if not html:
                typer.echo(f"[WARNING] Gagal fetch {url}")
                continue
                
            # Gunakan UniversalScraper untuk ekstraksi data
            data = scraper.extract_universal_data(html, url)
            
            if data:
                # Ringkas konten jika ada
                if data.get('content'):
                    from core.summarizer import Summarizer
                    summarizer = Summarizer()
                    data['summary'] = summarizer.summarize(data['content'])
                
                all_results.append(data)
                
            if idx < len(urls) - 1:
                time.sleep(delay)
        
        # Ekspor hasil
        if not all_results:
            typer.echo("[WARNING] Tidak ada data yang berhasil diekstrak")
            return
            
        try:
            if output.endswith('.csv'):
                Formatter.to_csv(all_results, output)
            elif output.endswith('.json'):
                Formatter.to_json(all_results, output)
            elif output.endswith('.md'):
                Formatter.to_md(all_results, output)
            elif output.endswith('.xlsx'):
                import pandas as pd
                pd.DataFrame(all_results).to_excel(output, index=False)
            else:
                # Default ke JSON
                Formatter.to_json(all_results, output.replace('.csv', '.json'))
                
            typer.echo(f"[SUCCESS] {len(all_results)} item disimpan ke {output}")
            
        except Exception as e:
            typer.echo(f"[ERROR] Gagal menyimpan file: {str(e)}")
            raise typer.Exit(1)

def batch_scrape(
    urls_file: str = typer.Option(..., "--file", "-f", help="File berisi daftar URL (satu per baris)"),
    output: str = typer.Option("batch_output.csv", help="Nama file output"),
    selenium: bool = typer.Option(False, "--selenium", "-s", help="Gunakan Selenium"),
    delay: int = typer.Option(2, "--delay", "-d", help="Delay antar request")
):
    """Scraping batch dari file daftar URL"""
    
    try:
        with open(urls_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
        if not urls:
            typer.echo("[ERROR] File kosong atau tidak ada URL valid")
            raise typer.Exit(1)
            
        # Gabungkan URL menjadi query
        query = ' '.join(urls)
        scrape(query=query, output=output, selenium=selenium, delay=delay)
        
    except FileNotFoundError:
        typer.echo(f"[ERROR] File {urls_file} tidak ditemukan")
        raise typer.Exit(1)

def test_scraper(
    url: str = typer.Option(..., "--url", "-u", help="URL untuk testing")
):
    """Test scraper pada satu URL"""
    
    from core.universal_scraper import UniversalScraper
    
    with UniversalScraper() as scraper:
        html = scraper.fetch_page(url)
        if html:
            data = scraper.extract_universal_data(html, url)
            typer.echo(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            typer.echo("[ERROR] Gagal fetch halaman")
