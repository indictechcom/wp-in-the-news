async function getNewsOfTheDay() {
    try {
        // Fetch the news data from the backend API
        const response = await fetch('/api/news_of_the_day');
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const newsList = await response.json();

        // Get the results container
        const resultsContainer = document.getElementById('results');
        resultsContainer.innerHTML = ''; // Clear previous results

        // Check if there are news items
        if (newsList.length === 0) {
            resultsContainer.innerHTML = '<p class="text-muted">No news available for today.</p>';
            return;
        }

        // Create a list to display the news items
        const ul = document.createElement('ul');
        ul.className = 'list-group';

        newsList.forEach(newsItem => {
            const li = document.createElement('li');
            li.className = 'list-group-item';

            // Add the news text
            const newsText = document.createElement('p');
            newsText.textContent = newsItem.text;
            li.appendChild(newsText);

            // Add the hyperlinks (if any)
            if (newsItem.links && newsItem.links.length > 0) {
                const linksContainer = document.createElement('div');
                linksContainer.className = 'mt-2';

                newsItem.links.forEach(link => {
                    const anchor = document.createElement('a');
                    // Prefix the link URL with "https://en.wikipedia.org/"
                    anchor.href = `https://en.wikipedia.org${link.url}`;
                    anchor.textContent = link.text;
                    anchor.target = '_blank'; // Open link in a new tab
                    anchor.className = 'btn btn-link btn-sm'; // Bootstrap styling
                    linksContainer.appendChild(anchor);
                });

                li.appendChild(linksContainer);
            }

            ul.appendChild(li);
        });

        resultsContainer.appendChild(ul);
    } catch (error) {
        console.error('Error fetching news:', error);
        const resultsContainer = document.getElementById('results');
        resultsContainer.innerHTML = '<p class="text-danger">Failed to load news. Please try again later.</p>';
    }
}

async function getNewsByDate(date) {
    try {
        // Fetch the news data for the given date from the backend API
        const response = await fetch(`/api/news/${date}`);
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const newsList = await response.json();

        // Get the results container
        const resultsContainer = document.getElementById('results');
        resultsContainer.innerHTML = ''; // Clear previous results

        // Check if there are news items
        if (newsList.length === 0) {
            resultsContainer.innerHTML = '<p class="text-muted">No news available for the selected date.</p>';
            return;
        }

        // Create a list to display the news items
        const ul = document.createElement('ul');
        ul.className = 'list-group';

        newsList.forEach(newsItem => {
            const li = document.createElement('li');
            li.className = 'list-group-item';

            // Add the news text
            const newsText = document.createElement('p');
            newsText.textContent = newsItem.text;
            li.appendChild(newsText);

            // Add the hyperlinks (if any)
            if (newsItem.links && newsItem.links.length > 0) {
                const linksContainer = document.createElement('div');
                linksContainer.className = 'mt-2';

                newsItem.links.forEach(link => {
                    const anchor = document.createElement('a');
                    // Prefix the link URL with "https://en.wikipedia.org/"
                    anchor.href = `https://en.wikipedia.org${link.url}`;
                    anchor.textContent = link.text;
                    anchor.target = '_blank'; // Open link in a new tab
                    anchor.className = 'btn btn-link btn-sm'; // Bootstrap styling
                    linksContainer.appendChild(anchor);
                });

                li.appendChild(linksContainer);
            }

            ul.appendChild(li);
        });

        resultsContainer.appendChild(ul);
    } catch (error) {
        console.error('Error fetching news by date:', error);
        const resultsContainer = document.getElementById('results');
        resultsContainer.innerHTML = '<p class="text-danger">Failed to load news for the specified date. Please try again later.</p>';
    }
}

function toggleDateSearchForm() {
    const dateSearchForm = document.getElementById('dateSearchForm');
    // Toggle the visibility of the date search form
    if (dateSearchForm.style.display === 'none' || dateSearchForm.style.display === '') {
        dateSearchForm.style.display = 'block';
    } else {
        dateSearchForm.style.display = 'none';
    }
}

function searchByDate() {
    const dateInput = document.getElementById('dateInput').value;
    if (!dateInput) {
        alert('Please select a date.');
        return;
    }
    // Call the getNewsByDate function with the selected date
    getNewsByDate(dateInput);
}