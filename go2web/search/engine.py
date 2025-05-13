from urllib.parse import quote_plus, parse_qs, urlparse, unquote
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
            href = a['href']
            if href.startswith('//'): # //duckduckgo.com...
                href = 'https:' + href # https://duckduckgo.com...
            parsed_href = urlparse(href)
            uddg = parse_qs(parsed_href.query).get('uddg', [None])[0]
            real_url = unquote(uddg) if uddg else href
            print(f"{i}. {a.get_text(strip=True)}\n   {real_url}")
    except Exception as e:
        print(f"Search failed: {e}")