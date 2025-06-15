document.addEventListener('DOMContentLoaded', () => {
  const searchBtn = document.getElementById('searchBtn');
  const queryInput = document.getElementById('query');
  const resultDiv = document.getElementById('result');

  // Focus the query input on popup open
  queryInput.focus();

  searchBtn.addEventListener('click', async () => {
    const query = queryInput.value.trim();
    
    if (!query) {
      showError('Please enter a research question');
      return;
    }

    // Clear previous results
    resultDiv.innerHTML = '';
    
    // Disable button during search
    searchBtn.disabled = true;
    searchBtn.textContent = 'Searching...';
    
    // Show loading state
    resultDiv.innerHTML = `
      <div class="loading">
        <div class="spinner"></div>
        <span>Researching "${truncate(query, 20)}"...</span>
      </div>
    `;

    try {
      const response = await fetch('http://127.0.0.1:8000/search/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          query: query,
          max_results: 5
        })
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      displayResults(data);
      
    } catch (error) {
      showError(`Failed to get results: ${error.message}<br><small>Make sure the research server is running</small>`);
    } finally {
      searchBtn.disabled = false;
      searchBtn.textContent = 'Search';
    }
  });

  function displayResults(data) {
    if (!data.results || data.results.length === 0) {
      resultDiv.innerHTML = '<div class="no-results">No relevant results found</div>';
      return;
    }

    let html = '';
    data.results.forEach(result => {
      html += `
        <div class="result-card">
          <h4><a href="${result.url}" target="_blank">${result.title || 'Untitled Source'}</a></h4>
          <div class="summary">${result.summary}</div>
          <div class="source">
            Source: <a href="${result.url}" target="_blank">${getDomain(result.url)}</a>
          </div>
        </div>
      `;
    });

    resultDiv.innerHTML = html;
  }

  function showError(message) {
    resultDiv.innerHTML = `<div class="error">${message}</div>`;
  }

  function truncate(str, n) {
    return str.length > n ? str.substring(0, n) + '...' : str;
  }

  function getDomain(url) {
    try {
      const domain = new URL(url).hostname.replace('www.', '');
      return domain;
    } catch {
      return url;
    }
  }
});