import sys
from core.client import HTTPClient
from core.cache import get_cache, set_cache
from parsers.content import parse_response
from search.engine import handle_search


def handle_help():
    print("""Usage:
  go2web -u <URL>         Make an HTTP request to the specified URL and print the response
  go2web -s <search-term> Search using DuckDuckGo and print top 10 results
  go2web -h               Show this help message""")


def handle_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    cached = get_cache(url)
    if cached:
        print("[*] Loaded from cache")
        print(cached)
        print("This is a cached response.")
        return

    client = HTTPClient()
    try:
        headers, body = client.make_request(url)
        parsed = parse_response(headers, body) 
        print(parsed)
        set_cache(url, parsed)
    except Exception as e:
        print(f"Error: {e}")


def main():
    if len(sys.argv) < 2 or sys.argv[1] == '-h':
        handle_help()
    elif sys.argv[1] == '-u' and len(sys.argv) >= 3:
        handle_url(sys.argv[2])
    elif sys.argv[1] == '-s' and len(sys.argv) >= 3:
        handle_search(" ".join(sys.argv[2:]))
    else:
        print("Invalid usage.\n")
        handle_help()


if __name__ == "__main__":
    main()