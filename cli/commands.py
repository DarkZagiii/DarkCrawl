"""
commands.py
Definisi perintah CLI (scrape, dsb).
"""

import typer

def scrape(
    query: str = typer.Option(..., "--query", "-q", help="Prompt perintah scraping atau URL"),
    output: str = typer.Option("output.csv", help="Nama file output hasil scrape"),
    plugin: str = typer.Option(None, help="Nama plugin (opsional)"),
):
    """Perintah scraping utama."""
    import os
    import re
    from core.crawler import Crawler
    from core.parser import Parser
    from core.plugin_loader import PluginLoader
    from core.summarizer import Summarizer
    from utils.formatter import Formatter

    typer.echo(f"[CLI] Menjalankan scrape: {query} | output: {output} | plugin: {plugin}")

    # Deteksi apakah input adalah URL atau prompt
    url_pattern = re.compile(r"https?://[\w\.-]+")
    if url_pattern.match(query):
        urls = [query]
    else:
        # Untuk v1: asumsikan prompt mengandung 1 URL, deteksi dengan regex
        urls = url_pattern.findall(query)
        if not urls:
            typer.echo("[ERROR] Tidak ada URL terdeteksi di prompt. Untuk v1, masukkan URL langsung.")
            raise typer.Exit(1)

    # Load plugin
    loader = PluginLoader(plugin_dir=os.path.abspath(os.path.join(os.path.dirname(__file__), '../plugins')))
    plugins = loader.load_plugins()
    if plugin:
        plugins = [p for p in plugins if p.__class__.__name__.lower().startswith(plugin.lower())]
        if not plugins:
            typer.echo(f"[ERROR] Plugin '{plugin}' tidak ditemukan.")
            raise typer.Exit(1)

    crawler = Crawler()
    parser = Parser()
    summarizer = Summarizer()
    all_results = []

    for url in urls:
        typer.echo(f"[CLI] Memproses: {url}")
        html = crawler.fetch(url)
        if not html:
            typer.echo(f"[ERROR] Gagal fetch {url}")
            continue
        # Pilih plugin yang match
        matched = None
        for p in plugins:
            if hasattr(p, 'match') and p.match(url):
                matched = p
                break
        if not matched:
            typer.echo(f"[ERROR] Tidak ada plugin yang cocok untuk {url}")
            continue
        # Ekstrak data
        data = matched.extract(html)
        if not data:
            typer.echo(f"[ERROR] Plugin gagal ekstrak data dari {url}")
            continue
        # Format data
        formatted = matched.format(data)
        # Jika artikel, tambahkan ringkasan
        if 'isi' in formatted:
            formatted['ringkasan'] = summarizer.summarize(formatted['isi'])
        all_results.append(formatted)

    # Ekspor
    if output.endswith('.csv'):
        Formatter.to_csv(all_results, output)
    elif output.endswith('.json'):
        Formatter.to_json(all_results, output)
    elif output.endswith('.md'):
        Formatter.to_md(all_results, output)
    else:
        typer.echo("[ERROR] Format output tidak didukung. Gunakan .csv, .json, atau .md")
        raise typer.Exit(1)

    typer.echo(f"[CLI] Selesai. Hasil disimpan di {output}")
