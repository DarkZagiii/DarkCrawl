import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    """Test homepage loads correctly"""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Universal Web Scraper' in rv.data

def test_scrape_no_url(client):
    """Test scrape endpoint with no URL"""
    rv = client.post('/scrape', json={})
    assert rv.status_code == 400
    assert b'URL tidak boleh kosong' in rv.data

def test_scrape_invalid_url(client):
    """Test scrape endpoint with invalid URL"""
    rv = client.post('/scrape', json={'url': 'invalid-url'})
    assert rv.status_code == 400

# Additional tests can be added for valid scraping, download endpoints, etc.
