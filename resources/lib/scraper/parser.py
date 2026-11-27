import re
from datetime import datetime
from html import unescape
from typing import List

from resources.lib.models import Dorf, Landkreis

BASE_URL = 'https://www.rbb-online.de'

_LANDKREIS_RE = re.compile(
    r'<area[^>]+href="(?P<url>/brandenburgaktuell/landschleicher/1000/(?P<slug>[^"/]+)\.html)"[^>]*alt="(?P<name>[^"]*)"')
_ARTICLE_RE = re.compile(
    r'datetime="(?P<datetime>[^"]*)".*?'
    r'href="(?P<url>[^"]+)"\s+class="sendeplatz".*?'
    r'<span class="manualteasertitle">(?P<name>.*?)</span>',
    re.DOTALL)


def parse_landkreise(html: str) -> List[Landkreis]:
    gefunden = {}
    for m in _LANDKREIS_RE.finditer(html):
        gefunden.setdefault(m['slug'], Landkreis(m['slug'], unescape(m['name']).strip(), BASE_URL + m['url']))
    return sorted(gefunden.values(), key=lambda l: l.name)


def parse_doerfer(html: str) -> List[Dorf]:
    doerfer = {}
    for article in html.split('<article')[1:]:
        m = _ARTICLE_RE.search(article)
        if m:
            doerfer.setdefault(
                m['url'], Dorf(unescape(m['name']).strip(), BASE_URL + m['url'], _format_datum(m['datetime'])))
    return sorted(doerfer.values(), key=lambda d: d.name.casefold())


def _format_datum(value: str) -> str:
    try:
        return datetime.fromisoformat(value).strftime('%d.%m.%Y')
    except ValueError:
        return value
