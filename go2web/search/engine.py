from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from core.client import HTTPClient


def handle_search(term):
    query = quote_plus(term)
    search_url = f"https://html.duckduckgo.com/html/?q={query}"
    client = HTTPClient()
    try:
        headers, body = client.make_request(search_url)
        soup = BeautifulSoup(body, 'html.parser')
        results = soup.find_all('a', class_='result__a', limit=10)
        for i, a in enumerate(results, 1):
            print(f"{i}. {a.get_text(strip=True)}\n   {a['href']}")
    except Exception as e:
        print(f"Search failed: {e}")