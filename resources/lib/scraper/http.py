import urllib.request

USER_AGENT = 'Mozilla/5.0'


def fetch(url: str, timeout: int = 20) -> str:
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode('utf-8', 'replace')
