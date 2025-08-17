document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const resultsContainer = document.getElementById('results-container');
    const paginationContainer = document.getElementById('pagination-container');
    const loader = document.getElementById('loader');
    let currentQuery = '';
    let currentPage = 1;

    function fetchAndRender(query, page=1) {
        resultsContainer.innerHTML = '';
        paginationContainer.innerHTML = '';
        loader.classList.remove('hidden');
        fetch(`/search?q=${encodeURIComponent(query)}&page=${page}`)
            .then(response => response.json())
            .then(data => {
                loader.classList.add('hidden');
                renderPage(data);
            })
            .catch(() => {
                loader.classList.add('hidden');
                resultsContainer.innerHTML = '<div class="result-card">An error occurred. Please try again.</div>';
            });
    }

    function renderPage(data) {
        resultsContainer.innerHTML = '';
        paginationContainer.innerHTML = '';
        const results = data.results;
        if (!results.length) {
            const noResultsMessage = `
                <div class="no-results-message">
                    <h3>No Results Found for Your Query</h3>
                    <p>DevSearch is currently a specialized search engine for developers, focused on topics like Python and JavaScript projects, tutorials, and resources.</p>
                    <p>We are constantly expanding our index. Thank you for your understanding!</p>
                </div>
            `;
            resultsContainer.innerHTML = noResultsMessage;
        } else {
            results.forEach(result => {
                const card = document.createElement('div');
                card.className = 'result-card';
                card.innerHTML = `
                    <a href="${result.url}" target="_blank" class="result-title">${result.title}</a>
                    <p class="result-url">${result.url}</p>
                    <p class="result-snippet"></p>
                `;
                card.querySelector('.result-snippet').innerHTML = result.snippet;
                resultsContainer.appendChild(card);
            });
        }
        // Pagination controls
        const totalPages = Math.ceil(data.total_results / 10);
        if (totalPages > 1) {
            const pagDiv = document.createElement('div');
            pagDiv.className = 'pagination';
            // Previous button
            const prevBtn = document.createElement('button');
            prevBtn.textContent = 'Previous';
            prevBtn.disabled = data.page === 1;
            prevBtn.className = 'pagination-btn';
            prevBtn.onclick = () => fetchAndRender(currentQuery, data.page - 1);
            pagDiv.appendChild(prevBtn);
            // Page numbers
            for (let i = 1; i <= totalPages; i++) {
                const pageBtn = document.createElement('button');
                pageBtn.textContent = i;
                pageBtn.className = 'pagination-btn';
                if (i === data.page) {
                    pageBtn.classList.add('active');
                }
                pageBtn.onclick = () => fetchAndRender(currentQuery, i);
                pagDiv.appendChild(pageBtn);
            }
            // Next button
            const nextBtn = document.createElement('button');
            nextBtn.textContent = 'Next';
            nextBtn.disabled = data.page === totalPages;
            nextBtn.className = 'pagination-btn';
            nextBtn.onclick = () => fetchAndRender(currentQuery, data.page + 1);
            pagDiv.appendChild(nextBtn);
            paginationContainer.appendChild(pagDiv);
        }
    }

    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        document.body.classList.add('results-active');
        const query = searchInput.value.trim();
        currentQuery = query;
        currentPage = 1;
        if (!query) {
            resultsContainer.innerHTML = '<div class="result-card">Please enter a search query.</div>';
            paginationContainer.innerHTML = '';
            return;
        }
        fetchAndRender(query, 1);
    });
});


