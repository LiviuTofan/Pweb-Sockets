import re
import html

def extract_readable_text_from_html(html_str: str) -> str:
    def clean_html(text: str) -> str:
        # Remove HTML tags
        text = re.sub('<[^>]*>', '', text)
        # Decode HTML entities
        return html.unescape(text).strip()

    # Remove scripts, styles, and other irrelevant elements
    html_str = re.sub('<script[^>]*>.*?</script>', '', html_str, flags=re.DOTALL)
    html_str = re.sub('<style[^>]*>.*?</style>', '', html_str, flags=re.DOTALL)
    html_str = re.sub('<head[^>]*>.*?</head>', '', html_str, flags=re.DOTALL)

    result = []

    # Extract title
    title_match = re.search('<title[^>]*>(.*?)</title>', html_str, re.DOTALL)
    if title_match:
        result.append(f"Title: {clean_html(title_match.group(1))}\n")

    # Extract text from key tags
    tags_to_extract = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'div']
    for tag in tags_to_extract:
        matches = re.findall(f'<{tag}[^>]*>(.*?)</{tag}>', html_str, re.DOTALL)
        for match in matches:
            cleaned_text = clean_html(match)
            if cleaned_text:
                result.append(f"{cleaned_text}\n")

    return '\n'.join(result).strip() or clean_html(html_str)


def clean_html_text(html_str: str) -> str:
    # Remove HTML tags
    text = re.sub('<[^>]*>', '', html_str)
    # Decode HTML entities
    return html.unescape(text).strip()