"""
formatter.py
Utilitas untuk format dan ekspor data (CSV, JSON, Markdown).
"""

import pandas as pd
import json

class Formatter:
    @staticmethod
    def to_csv(data, path):
        pd.DataFrame(data).to_csv(path, index=False)

    @staticmethod
    def to_json(data, path):
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def to_md(data, path):
        with open(path, "w") as f:
            for item in data:
                f.write(f"# {item.get('judul', item.get('nama', 'Data'))}\n\n")
                f.write(f"{item.get('isi', item.get('deskripsi', ''))}\n\n")
                f.write(f"Tanggal: {item.get('tanggal', '')}\n\n---\n\n")
