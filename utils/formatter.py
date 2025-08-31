"""
formatter.py
Utilitas untuk format dan ekspor data (CSV, JSON, Markdown, Excel).
"""

import pandas as pd
import json
from typing import List, Dict, Any

class Formatter:
    @staticmethod
    def to_csv(data: List[Dict[str, Any]], path: str):
        """Simpan data ke CSV"""
        try:
            df = pd.DataFrame(data)
            df.to_csv(path, index=False, encoding='utf-8')
        except Exception as e:
            print(f"Error saving CSV: {str(e)}")
            # Fallback: save as JSON
            Formatter.to_json(data, path.replace('.csv', '.json'))

    @staticmethod
    def to_json(data: List[Dict[str, Any]], path: str):
        """Simpan data ke JSON"""
        with open(path, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def to_md(data: List[Dict[str, Any]], path: str):
        """Simpan data ke Markdown"""
        with open(path, "w", encoding='utf-8') as f:
            for idx, item in enumerate(data):
                f.write(f"# {item.get('title', f'Data {idx+1}')}\n\n")
                
                # URL
                if item.get('url'):
                    f.write(f"**URL:** {item['url']}\n\n")
                
                # Description
                if item.get('description'):
                    f.write(f"**Description:** {item['description']}\n\n")
                
                # Content
                if item.get('content'):
                    f.write(f"**Content:**\n{item['content'][:500]}...\n\n")
                
                # Images
                if item.get('images'):
                    f.write("**Images:**\n")
                    for img in item['images'][:5]:
                        f.write(f"- {img.get('url', '')}\n")
                    f.write("\n")
                
                # Links
                if item.get('links'):
                    f.write("**Links:**\n")
                    for link in item['links'][:5]:
                        f.write(f"- [{link.get('text', 'Link')}]({link.get('url', '')})\n")
                    f.write("\n")
                
                # Metadata
                if item.get('extracted_at'):
                    f.write(f"**Extracted:** {item['extracted_at']}\n\n")
                
                f.write("---\n\n")

    @staticmethod
    def to_excel(data: List[Dict[str, Any]], path: str):
        """Simpan data ke Excel"""
        try:
            df = pd.DataFrame(data)
            
            # Flatten nested data for Excel
            for col in df.columns:
                if df[col].dtype == 'object':
                    try:
                        df[col] = df[col].apply(lambda x: str(x) if isinstance(x, (dict, list)) else x)
                    except:
                        pass
            
            df.to_excel(path, index=False, engine='openpyxl')
        except Exception as e:
            print(f"Error saving Excel: {str(e)}")
            Formatter.to_csv(data, path.replace('.xlsx', '.csv'))
