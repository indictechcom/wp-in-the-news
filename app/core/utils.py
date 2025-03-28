import hashlib
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

QOTD_API = 'https://en.wikipedia.org/w/api.php'
PARAMS = {
    "action": "parse",
    "format": "json",
    "page": "Wikipedia:In_the_news",
    "prop": "text",
    "formatversion": "2"
}

def fetch_news_of_the_day() -> dict:
    response = requests.get(QOTD_API, params=PARAMS)
    response.raise_for_status()
    data = response.json()
    news_html = data['parse']['text']
    return extract_news(news_html)

def extract_news(html_content: str) -> list[dict]:
    soup = BeautifulSoup(html_content, 'html.parser')
    news_list = []

    # Find the div with class floatright
    
    floatright_div = soup.find('div', class_='floatright')
    
    if floatright_div:
        news_ul = floatright_div.find('ul')
        if news_ul:
            # Find all list items within this ul
            news_items = news_ul.find_all('li')
        
            for item in news_items:
                # Extract the full text of the news item
                news_text = item.get_text(strip=True)
                
                # Skip empty items
                if not news_text:
                    continue
                
                # Extract all hyperlinks in the news item
                links = []
                for link_tag in item.find_all('a', href=True):
                    links.append({
                        "url": link_tag['href'],  # The hyperlink URL
                        "text": link_tag.get_text(strip=True)  # The hyperlink text
                    })
                
                # Create a unique ID for the news item
                unique_id = hashlib.md5(news_text.encode()).hexdigest()
                
                # Add the news item to the list
                news_list.append({
                    "id": unique_id,
                    "text": news_text,
                    "links": links  # List of all links in the news item
                })
    
      # Find the div with class "mw-content-ltr mw-parser-output"
    content_div = soup.find('div', class_='mw-content-ltr mw-parser-output')
    li_list = content_div.find_all('li')
    for li in li_list:
        code_block = li.find('code')
        if code_block:
            # print("Code Block:", code_block)

            # Extract and format the date
            featured_date = None
            match = re.search(r'date=(\d{1,2} \w+ \d{4})', code_block.text)
            if match:
                # Extract the date string
                raw_date = match.group(1)
                try:
                    # Parse the date and format it as "DD/MM.YYYY"
                    parsed_date = datetime.strptime(raw_date, "%d %B %Y")
                    featured_date = parsed_date.strftime("%Y-%m-%d")
                except ValueError:
                    print(f"Error parsing date: {raw_date}")

            # Add the formatted date to the news items
            for item in news_list:
                item["featured_date"] = featured_date
    
    for item in news_list:
        # Print the news item
        print(f"ID: {item['id']}")
        print(f"News: {item['text']}")
        
        # Print the associated links (if any)
        if item['links']:
            print("Links:")
            for link in item['links']:
                print(f"  - Text: {link['text']}, URL: {link['url']}")
        else:
            print("Links: None")
        
        print(f"Featured Date: {item.get('featured_date', 'N/A')}")
        
        print()  # Add a blank line for better readability

    return news_list