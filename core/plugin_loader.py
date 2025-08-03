"""
plugin_loader.py
Loader dinamis untuk plugin scraping.
"""

import importlib
import os

class PluginLoader:
    def __init__(self, plugin_dir="../plugins"):
        self.plugin_dir = plugin_dir

    def load_plugins(self):
        """Load semua plugin di folder plugins/"""
        plugins = []
        for fname in os.listdir(self.plugin_dir):
            if fname.endswith("_plugin.py"):
                modulename = fname[:-3]
                module = importlib.import_module(f"plugins.{modulename}")
                for attr in dir(module):
                    if attr.endswith("Plugin"):
                        plugins.append(getattr(module, attr)())
        return plugins
