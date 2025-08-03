"""
main.py
Entry point CLI untuk AI Scraper Framework.
"""


import typer
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import cli.commands as commands


# Multi-command CLI
app = typer.Typer()
app.add_typer(typer.Typer(), name="scrape")
app.command()(commands.scrape)

if __name__ == "__main__":
    import typer
    if len(sys.argv) == 1:
        # Mode interaktif
        url = input("[AI-Scraper] Masukkan URL yang ingin di-scrape: ")
        if not url.strip():
            print("[ERROR] URL tidak boleh kosong.")
            sys.exit(1)
        output = input("[AI-Scraper] Simpan hasil sebagai (output.csv/output.json/output.md): ")
        if not output.strip():
            output = "output.csv"
        # Jalankan scrape
        try:
            # Panggil fungsi scrape langsung
            commands.scrape(query=url, output=output, plugin=None)
        except Exception as e:
            print(f"[ERROR] Gagal scraping: {e}")
            sys.exit(1)
    else:
        app()
