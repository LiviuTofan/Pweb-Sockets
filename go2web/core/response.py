from typing import Dict

class HttpResponse:
    def __init__(self, status_code: int, headers: Dict[str, str], body: str):
        #Initialize a new HTTP response.
        self.status_code = status_code
        self.headers = headers
        self.body = body

    def get_readable_content(self) -> str:

        content_type = self.headers.get('Content-Type', '').lower()

        # Use the appropriate parser
        from go2web.parsers.json_parser import format_json
        from go2web.parsers.html_parser import extract_readable_text_from_html
        
        if 'application/json' in content_type:
            return format_json(self.body)
        elif 'text/html' in content_type:
            return extract_readable_text_from_html(self.body)
        else:
            return self.body