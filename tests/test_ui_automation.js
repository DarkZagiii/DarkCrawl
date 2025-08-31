const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();

  try {
    // Navigate to the web app
    await page.goto('http://localhost:5000', { waitUntil: 'networkidle2' });

    // Check homepage title
    const title = await page.title();
    if (!title.includes('Universal Web Scraper')) {
      throw new Error('Homepage title does not match');
    }

    // Input URL to scrape
    await page.type('#url-input', 'https://shopee.co.id');
    await page.select('#format-select', 'json');

    // Click start scraping button
    await page.click('#start-scraping-btn');

    // Wait for results table to appear
    await page.waitForSelector('#results-tbody tr', { timeout: 30000 });

    // Check if results are displayed
    const rows = await page.$$eval('#results-tbody tr', trs => trs.length);
    if (rows === 0) {
      throw new Error('No scraping results found');
    }

    // Check analysis section visible
    const analysisVisible = await page.$eval('#insights-section', el => window.getComputedStyle(el).display !== 'none');
    if (!analysisVisible) {
      throw new Error('Analysis section not visible');
    }

    console.log('UI automation test passed');
  } catch (err) {
    console.error('UI automation test failed:', err);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
