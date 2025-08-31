#!/usr/bin/env python3
"""
Main CLI entry point untuk universal web scraper
"""

import typer
from cli.commands import scrape, batch_scrape, test_scraper

# Create typer app
app = typer.Typer(
    name="Universal Web Scraper",
    help="Scraper universal untuk semua jenis website",
    no_args_is_help=True
)

# Register commands
app.command()(scrape)
app.command("batch-scrape")(batch_scrape)
app.command("test-scraper")(test_scraper)

if __name__ == "__main__":
    app()
