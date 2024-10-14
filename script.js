const searchBox = document.getElementById('search-box');
const searchButton = document.getElementById('search-button');
const resultsDiv = document.getElementById('results');

searchButton.addEventListener('click', () => {
    const query = searchBox.value;

    // Make an AJAX request to your Python backend
    fetch(`/search/?q=${query}`)
        .then(response => response.json())
        .then(data => {
            // Assuming the API response is an array of result objects
            displayResults(data.results);
        })
        .catch(error => {
            console.error('Error fetching search results:', error);
            resultsDiv.textContent = 'Error fetching search results.';
        });
});

function displayResults(results) {
    resultsDiv.innerHTML = ''; // Clear previous results

    if (results.length > 0) {
        results.forEach(result => {
            const resultItem = document.createElement('div');
            resultItem.classList.add('result-item');

            const link = document.createElement('a');
            link.href = result.filepath;
            link.textContent = result.filename;
            link.target = '_blank'; // Open link in new tab

            resultItem.appendChild(link);
            resultItem.appendChild(document.createTextNode(` - ${result.description}`));

            resultsDiv.appendChild(resultItem);
        });
    } else {
        resultsDiv.textContent = 'No results found.';
    }
}