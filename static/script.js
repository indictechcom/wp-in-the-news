// Helper to clear container content safely
function clearElement(element) {
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}

// Helper to create and append a message to a container
function appendMessage(container, message, className) {
    const p = document.createElement('p');
    p.className = className;
    p.textContent = message;
    container.appendChild(p);
}

// Display a list of news items
function displayNewsList(newsList, container) {
    const ul = document.createElement('ul');
    ul.className = 'list-group';

    newsList.forEach(newsItem => {
        const li = document.createElement('li');
        li.className = 'list-group-item';

        const newsText = document.createElement('p');
        newsText.textContent = newsItem.text;
        li.appendChild(newsText);

        if (newsItem.links && newsItem.links.length > 0) {
            const linksContainer = document.createElement('div');
            linksContainer.className = 'mt-2';

            newsItem.links.forEach(link => {
                const anchor = document.createElement('a');
                anchor.href = `https://en.wikipedia.org${link.url}`;
                anchor.textContent = link.text;
                anchor.target = '_blank';
                anchor.className = 'btn btn-link btn-sm';
                linksContainer.appendChild(anchor);
            });

            li.appendChild(linksContainer);
        }

        ul.appendChild(li);
    });

    container.appendChild(ul);
}

// Fetch and display news of the day
async function getNewsOfTheDay() {
    const resultsContainer = document.getElementById('results');
    clearElement(resultsContainer);

    try {
        const response = await fetch('/api/news_of_the_day');
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const newsList = await response.json();

        if (newsList.length === 0) {
            appendMessage(resultsContainer, 'No news available for today.', 'text-muted');
            return;
        }

        displayNewsList(newsList, resultsContainer);
    } catch (error) {
        console.error('Error fetching news:', error);
        appendMessage(resultsContainer, 'Failed to load news. Please try again later.', 'text-danger');
    }
}

// Fetch and display news by selected date
async function getNewsByDate(date) {
    const resultsContainer = document.getElementById('results');
    clearElement(resultsContainer);

    try {
        const response = await fetch(`/api/news/${date}`);
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const newsList = await response.json();

        if (newsList.length === 0) {
            appendMessage(resultsContainer, 'No news available for the selected date.', 'text-muted');
            return;
        }

        displayNewsList(newsList, resultsContainer);
    } catch (error) {
        console.error('Error fetching news by date:', error);
        appendMessage(resultsContainer, 'Failed to load news for the specified date. Please try again later.', 'text-danger');
    }
}

// Toggle visibility of date input form
function toggleDateSearchForm() {
    const form = document.getElementById('dateSearchForm');
    form.style.display = (form.style.display === 'none' || form.style.display === '') ? 'block' : 'none';
}

// Handle search button click for date-based news
function searchByDate() {
    const date = document.getElementById('dateInput').value;
    if (!date) {
        alert('Please select a date.');
        return;
    }
    getNewsByDate(date);
}
