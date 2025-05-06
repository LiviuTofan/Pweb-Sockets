import time
import pickle
from typing import Dict, Optional
import os

from go2web.core.response import HttpResponse

class CacheEntry:

    def __init__(self, response: HttpResponse, expiry_seconds: int = 300):

        self.response = response
        self.expiry_time = time.time() + expiry_seconds

    def is_expired(self) -> bool:
        return time.time() > self.expiry_time


class Cache:
    DEFAULT_CACHE_FILE = 'go2web_cache.pkl'
    
    def __init__(self, cache_file: str = None):

        self.cache_file = cache_file or self.DEFAULT_CACHE_FILE
        self.cache: Dict[str, CacheEntry] = {}
        self.load_from_file()
    
    def get(self, url: str) -> Optional[HttpResponse]:
        # Get a response from the cache if it exists and is not expired.
        entry = self.cache.get(url)
        if entry and not entry.is_expired():
            print("CACHE HIT FOUND AND LOADED!")
            return entry.response
        return None
    
    def set(self, url: str, response: HttpResponse, expiry_seconds: int = 300) -> None:
        #Store a response in the cache.
        self.cache[url] = CacheEntry(response, expiry_seconds)
    
    def load_from_file(self) -> None:
        #Load the cache from disk if the cache file exists.
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'rb') as f:
                    self.cache = pickle.load(f)
        except (FileNotFoundError, pickle.PickleError):
            self.cache = {}
    
    def save_to_file(self) -> None:
        with open(self.cache_file, 'wb') as f:
            pickle.dump(self.cache, f)