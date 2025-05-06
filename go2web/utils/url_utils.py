import html
import urllib.parse

def normalize_url(url: str) -> str:
    if not url.startswith(('http://', 'https://')):
        return f'https://{url}'
    return url

def clean_url(url: str) -> str:
    # Decode HTML entities
    url = html.unescape(url)
    
    # Remove tracking parameters
    amp_rut_index = url.find("&rut=")
    if amp_rut_index != -1:
        url = url[:amp_rut_index]
    
    return url

def extract_redirect_url(url: str) -> str:
    if 'uddg=' in url:
        start = url.index('uddg=') + 5
        encoded_url = url[start:]
        return urllib.parse.unquote(encoded_url)
    return url

def handle_redirect_url(base_url: str, redirect_url: str) -> str:
    if not redirect_url.startswith('http'):
        parsed_base = urllib.parse.urlparse(base_url)
        base_domain = f"{parsed_base.scheme}://{parsed_base.netloc}"
        
        if redirect_url.startswith('/'):
            return f"{base_domain}{redirect_url}"
        else:
            return f"{base_domain}/{redirect_url}"
    return redirect_url