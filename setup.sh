#!/bin/bash
# Setup script for E-Commerce Scraper
# Simplified setup with easy instructions
# Setup dan Run Darkcrawl Framework

echo "🕷️ Darkcrawl - Universal Web Scraper Framework"
echo "================================================"

# 1. Create Virtual Environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv .venv

# 2. Activate Virtual Environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# 3. Install Dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Initialize Database
echo "💾 Initializing database..."
python3 -c "from core.database import Database; db = Database(); print('Database initialized ✓')"

# 5. Run CLI Test
echo ""
echo "✅ Testing CLI..."
python3 -m cli.main list-plugins

# 6. Start Web Server
echo ""
echo "🌐 Starting Darkcrawl Web Server..."
echo "📌 Open: http://localhost:5000"
python3 -m web.app

