import urllib.request

USER_AGENT = 'Mozilla/5.0'


def fetch(url: str, timeout: int = 20) -> str:
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode('utf-8', 'replace')


def fetch_head(url: str, limit: int = 16384, timeout: int = 20) -> str:
    """Reads only the beginning of a page, enough for the <head> meta tags."""
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read(limit).decode('utf-8', 'replace')
