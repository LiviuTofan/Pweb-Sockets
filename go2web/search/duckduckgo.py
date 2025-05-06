import re
import urllib.parse
from typing import List

from go2web.core.http_client import HttpClient
from go2web.parsers.html_parser import clean_html_text
from go2web.utils.url_utils import clean_url, extract_redirect_url

class SearchResult:

    def __init__(self, title: str, url: str, description: str):
        self.title = title
        self.url = url
        self.description = description


class DuckDuckGoSearch:

    def __init__(self, http_client: HttpClient):
        self.http_client = http_client
    
    def search(self, search_term: str) -> List[SearchResult]:
        encoded_term = urllib.parse.quote(search_term)
        search_url = f"https://duckduckgo.com/html/?q={encoded_term}"
        
        response = self.http_client.fetch_url(search_url)
        if not response or response.status_code != 200:
            print(f"Search failed with status code: {response.status_code if response else 'N/A'}")
            return []
        
        return self.extract_search_results(response.body)
    
    def extract_search_results(self, html_str: str) -> List[SearchResult]:
        results = []
        pattern = re.compile(
            r'<h2 class="result__title">.*?<a.*?href="(.*?)".*?>(.*?)</a>.*?<a.*?class="result__snippet".*?>(.*?)</a>',
            re.DOTALL
        )
        
        for match in pattern.finditer(html_str):
            url, title, description = match.groups()
            
            # Clean and process URL
            if url.startswith('//duckduckgo.com/l/?uddg='):
                url = extract_redirect_url(url)
            
            url = clean_url(url)
            title = clean_html_text(title)
            description = clean_html_text(description)
            
            results.append(SearchResult(title, url, description))
        
        return results