import urllib.request
from http.client import HTTPException
from typing import Optional

USER_AGENT = 'Mozilla/5.0'


def _read(url: str, limit: Optional[int], timeout: int) -> str:
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read(limit).decode('utf-8', 'replace')
    except HTTPException as e:
        # Callers only handle OSError (which URLError and socket timeouts already are)
        raise OSError(str(e)) from e


def fetch(url: str, timeout: int = 20) -> str:
    return _read(url, None, timeout)


def fetch_head(url: str, limit: int = 16384, timeout: int = 20) -> str:
    """Reads only the beginning of a page, enough for the <head> meta tags."""
    return _read(url, limit, timeout)
