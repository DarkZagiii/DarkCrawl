class WebScraperApp {
    constructor() {
        this.currentData = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.setupUI();
    }

    bindEvents() {
        document.getElementById('start-scraping').addEventListener('click', () => this.startScraping());
        document.getElementById('search-input').addEventListener('input', (e) => this.filterData(e.target.value));
        document.getElementById('category-filter').addEventListener('change', (e) => this.filterByCategory(e.target.value));
        
        // Download buttons
        document.getElementById('download-json').addEventListener('click', () => this.downloadData('json'));
        document.getElementById('download-csv').addEventListener('click', () => this.downloadData('csv'));
        document.getElementById('download-excel').addEventListener('click', () => this.downloadData('xlsx'));
    }

    setupUI() {
        // Sembunyikan section yang tidak perlu saat load
        document.getElementById('progress-section').style.display = 'none';
        document.getElementById('results-section').style.display = 'none';
        document.getElementById('insights-section').style.display = 'none';
    }

    async startScraping() {
        const url = document.getElementById('url-input').value;
        const format = document.getElementById('output-format').value;
        const useSelenium = document.getElementById('use-selenium').checked;
        const delay = document.getElementById('delay-input').value;

        if (!url) {
            alert('Mohon masukkan URL yang valid');
            return;
        }

        // Tampilkan progress section
        document.getElementById('progress-section').style.display = 'block';
        document.getElementById('results-section').style.display = 'none';
        document.getElementById('insights-section').style.display = 'none';

        document.getElementById('progress-text').innerText = 'Mengambil data dari website...';
        document.getElementById('progress-fill').style.width = '0%';

        try {
            const response = await fetch('/scrape', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    url: url,
                    use_selenium: useSelenium,
                    delay: parseInt(delay),
                    format: format
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                alert('Error: ' + (errorData.error || 'Gagal scraping'));
                this.resetUI();
                return;
            }

            const result = await response.json();
            this.currentData = result.data;

            // Update UI dengan hasil
            this.showResults(result);
            this.populateCategoryFilter(result.summary.categories);
            this.showInsights(result.summary);

        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            this.resetUI();
        }
    }

    resetUI() {
        document.getElementById('progress-section').style.display = 'none';
    }

    showResults(result) {
        document.getElementById('results-section').style.display = 'block';

        // Update summary cards
        document.getElementById('total-products').innerText = result.summary.total_products;
        document.getElementById('total-categories').innerText = Object.keys(result.summary.categories).length;
        document.getElementById('total-images').innerText = result.summary.statistics.total_images;
        document.getElementById('total-links').innerText = result.summary.statistics.total_links;

        // Render table data
        this.renderTable(this.currentData.products);
    }

    populateCategoryFilter(categories) {
        const filter = document.getElementById('category-filter');
        filter.innerHTML = '<option value="">Semua Kategori</option>';
        Object.keys(categories).forEach(cat => {
            const option = document.createElement('option');
            option.value = cat;
            option.textContent = cat + ' (' + categories[cat] + ')';
            filter.appendChild(option);
        });
    }

    showInsights(summary) {
        document.getElementById('insights-section').style.display = 'block';
        if (summary.categories && Object.keys(summary.categories).length > 0) {
            document.getElementById('top-category').innerText = Object.keys(summary.categories).reduce((a, b) => summary.categories[a] > summary.categories[b] ? a : b, '');
        } else {
            document.getElementById('top-category').innerText = '-';
        }
        if (summary.statistics && summary.statistics.avg_price) {
            document.getElementById('avg-price').innerText = summary.statistics.avg_price;
        } else {
            document.getElementById('avg-price').innerText = 'Rp -';
        }
        document.getElementById('platform').innerText = summary.platform || 'Universal';
    }

    renderTable(products) {
        const tbody = document.getElementById('results-tbody');
        tbody.innerHTML = '';

        products.forEach(product => {
            const tr = document.createElement('tr');

            // Gambar
            const tdImg = document.createElement('td');
            if (product.images && product.images.length > 0) {
                const img = document.createElement('img');
                img.src = product.images[0].url || '';
                img.alt = product.title || 'Image';
                img.style.width = '80px';
                img.style.height = 'auto';
                tdImg.appendChild(img);
            }
            tr.appendChild(tdImg);

            // Produk
            const tdTitle = document.createElement('td');
            tdTitle.textContent = product.title || '-';
            tr.appendChild(tdTitle);

            // Kategori
            const tdCategory = document.createElement('td');
            tdCategory.textContent = product.category || '-';
            tr.appendChild(tdCategory);

            // Harga
            const tdPrice = document.createElement('td');
            tdPrice.textContent = product.price || '-';
            tr.appendChild(tdPrice);

            // Deskripsi
            const tdDesc = document.createElement('td');
            tdDesc.textContent = product.description || '-';
            tr.appendChild(tdDesc);

            // Aksi
            const tdAction = document.createElement('td');
            const btnDetail = document.createElement('button');
            btnDetail.textContent = 'Detail';
            btnDetail.className = 'btn-primary';
            btnDetail.addEventListener('click', () => this.showProductDetail(product));
            tdAction.appendChild(btnDetail);
            tr.appendChild(tdAction);

            tbody.appendChild(tr);
        });
    }

    filterData(searchTerm) {
        if (!this.currentData) return;
        const filtered = this.currentData.products.filter(p => p.title.toLowerCase().includes(searchTerm.toLowerCase()));
        this.renderTable(filtered);
    }

    filterByCategory(category) {
        if (!this.currentData) return;
        if (!category) {
            this.renderTable(this.currentData.products);
            return;
        }
        const filtered = this.currentData.products.filter(p => p.category === category);
        this.renderTable(filtered);
    }

    showProductDetail(product) {
        const modal = document.getElementById('product-modal');
        const modalBody = document.getElementById('modal-body');
        modalBody.innerHTML = `
            <h4>${product.title}</h4>
            <p><strong>Harga:</strong> ${product.price}</p>
            <p><strong>Kategori:</strong> ${product.category}</p>
            <p><strong>Deskripsi:</strong> ${product.description}</p>
            <p><strong>URL:</strong> <a href="${product.metadata.url}" target="_blank">${product.metadata.url}</a></p>
            <p><strong>Jumlah Kata:</strong> ${product.metadata.word_count}</p>
            <div>
                <strong>Gambar:</strong><br/>
                ${product.images.map(img => `<img src="${img.url}" alt="${img.alt}" style="width:100px; margin:5px;">`).join('')}
            </div>
        `;
        modal.style.display = 'block';

        // Close modal event
        const closeBtn = modal.querySelector('.close');
        closeBtn.onclick = () => {
            modal.style.display = 'none';
        };
        window.onclick = (event) => {
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        };
    }

    downloadData(format) {
        if (!this.currentData) return;
        const url = `/download/scraped_data.${format}`;
        window.open(url, '_blank');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new WebScraperApp();
});
