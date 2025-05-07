import argparse
import sys

from go2web.core.http_client import HttpClient
from go2web.core.cache import Cache
from go2web.search.duckduckgo import DuckDuckGoSearch

def main():
    """Main entry point for the Go2Web utility."""
    parser = argparse.ArgumentParser(description='Go2Web: Web Utility Tool')
    parser.add_argument('-u', dest='url', help='Fetch and print URL content')
    parser.add_argument('-s', dest='search', help='Search using DuckDuckGo')
    parser.add_argument('--show-help', action='store_true', help='Show help')

    args = parser.parse_args()
    
    # Initialize components
    cache = Cache()
    http_client = HttpClient(cache)
    
    try:
        if args.show_help:
            parser.print_help()
        elif args.url:
            url = args.url
            print(f"Fetching: {url}")
            response = http_client.fetch_url(url)
            if response:
                print(response.get_readable_content())
            else:
                print("Failed to fetch the URL.")
        elif args.search:
            search_term = args.search
            search_engine = DuckDuckGoSearch(http_client)
            results = search_engine.search(search_term)
            
            if results:
                print(f"Search results for: {search_term}")
                print("------------------------------------")
                
                for i, result in enumerate(results[:10], 1):
                    print(f"{i}. {result.title}")
                    print(f"   {result.url}")
                    print(f"   {result.description}\n")
                
                # User result selection
                try:
                    choice = input("Enter a number to open the result (1-10), or 'q' to quit: ").strip()
                    if choice.lower() == 'q':
                        return
                    
                    result_num = int(choice)
                    if 1 <= result_num <= min(10, len(results)):
                        selected_result = results[result_num - 1]
                        print(f"Fetching: {selected_result.url}")
                        
                        selected_response = http_client.fetch_url(selected_result.url)
                        if selected_response:
                            print(selected_response.get_readable_content())
                        else:
                            print("Failed to fetch the selected result.")
                    else:
                        print("Invalid result number")
                except ValueError:
                    print("Invalid input")
            else:
                print("No search results found.")
        else:
            parser.print_help()
    finally:
        # Save cache before exiting
        cache.save_to_file()

if __name__ == '__main__':
    main()