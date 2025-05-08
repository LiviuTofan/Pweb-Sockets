import socket
import ssl
import re
from typing import Optional, Tuple
from urllib.parse import urlparse

from go2web.core.response import HttpResponse
from go2web.core.cache import Cache
from go2web.utils.url_utils import normalize_url, handle_redirect_url

class HttpClient:

    HTTP_PORT = 80
    HTTPS_PORT = 443
    MAX_REDIRECTS = 5
    USER_AGENT = 'Go2Web/1.0'
    
    def __init__(self, cache: Optional[Cache] = None):
        self.cache = cache or Cache()
    
    def fetch_url(self, url: str, redirect_count: int = 0) -> Optional[HttpResponse]:
        if redirect_count > self.MAX_REDIRECTS:
            raise Exception("Too many redirects")
        
        url = normalize_url(url)
        
        # Check cache
        cached_response = self.cache.get(url)
        if cached_response:
            return cached_response
        
        # Parse URL for connection
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        path = parsed_url.path or '/'
        if parsed_url.query:
            path += f'?{parsed_url.query}'
        
        is_https = url.startswith('https://')
        port = parsed_url.port or (self.HTTPS_PORT if is_https else self.HTTP_PORT)
        
        # Create SSL context for HTTPS
        context = ssl.create_default_context() if is_https else None
        
        try:
            with socket.create_connection((host, port)) as sock:
                if is_https:
                    sock = context.wrap_socket(sock, server_hostname=host)
                
                request = (
                    f"GET {path} HTTP/1.1\r\n"
                    f"Host: {host}\r\n"
                    f"User-Agent: {self.USER_AGENT}\r\n"
                    f"Connection: close\r\n"
                    f"Accept: text/html,application/json\r\n\r\n"
                )
                sock.sendall(request.encode())
                
                response = b''
                while True:
                    chunk = sock.recv(4096)
                    if not chunk:
                        break
                    response += chunk
                
                response_str = response.decode('utf-8', errors='ignore')
                parsed_response = self._parse_response(response_str)
                
                # Handle redirects
                if 300 <= parsed_response.status_code < 400:
                    redirect_url = parsed_response.headers.get('Location')
                    if redirect_url:
                        if not redirect_url.startswith('http'):
                            redirect_url = f"{parsed_url.scheme}://{host}{redirect_url if redirect_url.startswith('/') else f'/{redirect_url}'}"
                        return self.fetch_url(redirect_url, redirect_count + 1)
                
                # Cache the response
                self.cache.set(url, parsed_response)
                return parsed_response
                
        except Exception as e:
            print(f"Error fetching URL: {e}")
            return None
    
    def _parse_response(self, response_str: str) -> HttpResponse:
        # Split headers and body - find the first occurrence of double line break
        header_end = response_str.find('\r\n\r\n')
        if header_end == -1:
            header_end = response_str.find('\n\n')
        
        if header_end == -1:
            return HttpResponse(500, {}, "Invalid response from server")
        
        headers_str = response_str[:header_end]
        body = response_str[header_end + (4 if '\r\n\r\n' in response_str[:header_end+4] else 2):]
        
        # Parse status line
        status_match = re.match(r'HTTP/\d\.\d\s+(\d+)\s+(.+)', headers_str.split('\n')[0])
        if not status_match:
            return HttpResponse(500, {}, "Invalid status line")
        
        status_code = int(status_match.group(1))
        headers = {}
        for line in headers_str.split('\n')[1:]:
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()
        
        return HttpResponse(status_code, headers, body)