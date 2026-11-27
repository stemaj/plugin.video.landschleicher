import sys
from urllib.parse import parse_qsl, urlencode

import xbmcgui
import xbmcplugin

from resources.lib.scraper import http, parser
from resources.lib.scraper.parser import BASE_URL
from resources.lib.utils import kodilogging, kodiutils

ROOT_URL = BASE_URL + '/brandenburgaktuell/landschleicher/'

BASE = sys.argv[0]
HANDLE = int(sys.argv[1])


def build_url(**params) -> str:
    return f'{BASE}?{urlencode(params)}'


def show_landkreise() -> None:
    for landkreis in parser.parse_landkreise(http.fetch(ROOT_URL)):
        item = xbmcgui.ListItem(label=landkreis.name)
        xbmcplugin.addDirectoryItem(HANDLE, build_url(action='landkreis', url=landkreis.url), item, True)
    xbmcplugin.endOfDirectory(HANDLE)


def show_doerfer(url: str) -> None:
    for dorf in parser.parse_doerfer(http.fetch(url)):
        item = xbmcgui.ListItem(label=f'{dorf.name} ({dorf.datum})')
        item.getVideoInfoTag().setTitle(dorf.name)
        xbmcplugin.addDirectoryItem(HANDLE, build_url(action='dorf', url=dorf.url), item, False)
    xbmcplugin.endOfDirectory(HANDLE)


def run() -> None:
    kodilogging.config()
    params = dict(parse_qsl(sys.argv[2].lstrip('?')))
    action = params.get('action')
    try:
        if action is None:
            show_landkreise()
        elif action == 'landkreis' and params.get('url', '').startswith(ROOT_URL):
            show_doerfer(params['url'])
        else:
            xbmcplugin.endOfDirectory(HANDLE, succeeded=False)
    except OSError as e:
        kodiutils.notification('Landschleicher', str(e))
        xbmcplugin.endOfDirectory(HANDLE, succeeded=False)
