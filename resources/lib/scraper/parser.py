import re
from datetime import datetime
from html import unescape
from typing import List, Tuple

from resources.lib.models import Dorf, Landkreis

BASE_URL = 'https://www.rbb-online.de'

_LANDKREIS_RE = re.compile(
    r'<area[^>]+href="(?P<url>/brandenburgaktuell/landschleicher/1000/(?P<slug>[^"/]+)\.html)"[^>]*alt="(?P<name>[^"]*)"')
_ARTICLE_RE = re.compile(
    r'datetime="(?P<datetime>[^"]*)".*?'
    r'href="(?P<url>[^"]+)"\s+class="sendeplatz".*?'
    r'<span class="manualteasertitle">(?P<name>.*?)</span>',
    re.DOTALL)
_VIDEO_RE = re.compile(r'"contentUrl":\s*"(https://[^"]+)"')
_NEUESTE_RE = re.compile(
    r'<h3 class="manualteasertitle">\s*<a href="(?P<url>[^"]+)" class="sendeplatz">\s*(?P<name>[^<]*?)\s*<')


def parse_landkreise(html: str) -> List[Landkreis]:
    gefunden = {}
    for m in _LANDKREIS_RE.finditer(html):
        gefunden.setdefault(m['slug'], Landkreis(m['slug'], unescape(m['name']).strip(), BASE_URL + m['url']))
    return list(gefunden.values())


def parse_doerfer(html: str) -> List[Dorf]:
    doerfer = {}
    for article in html.split('<article')[1:]:
        m = _ARTICLE_RE.search(article)
        if m:
            doerfer.setdefault(m['url'], Dorf(unescape(m['name']).strip(), BASE_URL + m['url'], m['datetime']))
    return list(doerfer.values())


def parse_neueste(html: str) -> List[Dorf]:
    """Parses the 'Die neuesten Folgen' ticker of the start page, newest first."""
    doerfer = {}
    for m in _NEUESTE_RE.finditer(html):
        doerfer.setdefault(m['url'], Dorf(unescape(m['name']).strip(), BASE_URL + m['url'], ''))
    return list(doerfer.values())


def parse_meta(html: str) -> Tuple[str, str]:
    """Returns (beschreibung, bild) from the Open Graph tags of a Beitrag page."""
    return _og(html, 'description'), _og(html, 'image')


def parse_video_url(html: str) -> str:
    """Returns the stream URL from the JSON-LD block of a Beitrag page, or '' if there is no video."""
    m = _VIDEO_RE.search(html)
    return m[1] if m else ''


def _og(html: str, prop: str) -> str:
    m = re.search(rf'<meta property="og:{prop}" content="([^"]*)"', html)
    return unescape(m[1]).strip() if m else ''


def format_datum(value: str) -> str:
    try:
        return datetime.fromisoformat(value).strftime('%d.%m.%Y')
    except ValueError:
        return value
