import sys
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import parse_qsl, urlencode

import xbmc
import xbmcgui
import xbmcplugin

from resources.lib.cache import DetailCache
from resources.lib.models import Dorf
from resources.lib.scraper import http, parser
from resources.lib.scraper.parser import BASE_URL
from resources.lib.utils import kodilogging, kodiutils

MAX_WORKERS = 10
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


def fetch_details(dorf: Dorf):
    try:
        return dorf.url, parser.parse_meta(http.fetch_head(dorf.url))
    except OSError:
        return dorf.url, None


def show_doerfer(url: str) -> None:
    cache = DetailCache()
    doerfer = [cache.apply(d) for d in parser.parse_doerfer(http.fetch(url))]
    for dorf in doerfer:
        item = xbmcgui.ListItem(label=f'{dorf.name} ({dorf.datum})')
        tag = item.getVideoInfoTag()
        tag.setTitle(dorf.name)
        tag.setPlot(dorf.beschreibung)
        if dorf.bild:
            item.setArt({'thumb': dorf.bild, 'poster': dorf.bild})
        xbmcplugin.addDirectoryItem(HANDLE, build_url(action='dorf', url=dorf.url), item, False)
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)
    nachladen([d for d in doerfer if d.url not in cache], cache, BASE + sys.argv[2])


def nachladen(fehlende, cache: DetailCache, folder_path: str) -> None:
    """Loads missing details after the list is shown, then refreshes the list if it is still open."""
    if not fehlende:
        return
    monitor = xbmc.Monitor()
    neu = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        for url, meta in pool.map(fetch_details, fehlende):
            if meta is not None:
                cache.put(url, *meta)
                neu += 1
            if monitor.abortRequested():
                break
    if neu:
        cache.save()
        if xbmc.getInfoLabel('Container.FolderPath') == folder_path:
            xbmc.executebuiltin('Container.Refresh')


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
