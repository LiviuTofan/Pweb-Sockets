import os
import hashlib

CACHE_DIR = ".go2web_cache"


def _hash_key(url):
    return hashlib.sha256(url.encode()).hexdigest()


def get_cache(url):
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, _hash_key(url))
    return open(path, 'r', encoding='utf-8').read() if os.path.exists(path) else None


def set_cache(url, content):
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, _hash_key(url))
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)