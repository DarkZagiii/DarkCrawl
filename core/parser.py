"""
parser.py
Parser HTML universal menggunakan BeautifulSoup.
"""

from bs4 import BeautifulSoup

class Parser:
    def __init__(self, parser="lxml"):
        self.parser = parser

    def parse(self, html):
        """Parse HTML dan kembalikan objek BeautifulSoup."""
        return BeautifulSoup(html, self.parser)
