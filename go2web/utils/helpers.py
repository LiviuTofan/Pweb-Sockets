def normalize_url(url):
    """Ensure URL starts with http:// or https://"""
    if not url.startswith("http://") and not url.startswith("https://"):
        return "https://" + url
    return url