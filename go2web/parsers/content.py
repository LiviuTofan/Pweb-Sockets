import json
from bs4 import BeautifulSoup


def clean_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text(separator='\n', strip=True)


def parse_response(headers, body):
    for line in headers.splitlines():
        if 'Content-Type:' in line:
            if 'application/json' in line:
                try:
                    return json.dumps(json.loads(body), indent=2)
                except:
                    return body
    return clean_html(body)