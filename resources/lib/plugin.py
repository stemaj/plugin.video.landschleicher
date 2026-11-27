import logging
import sys
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import parse_qsl, urlencode

import xbmc
import xbmcgui
import xbmcplugin

from resources.lib import player, search, sorting, strings
from resources.lib.cache import DetailCache
from resources.lib.models import Dorf
from resources.lib.scraper import http, parser
from resources.lib.scraper.parser import BASE_URL
from resources.lib.utils import kodilogging, kodiutils

logger = logging.getLogger(__name__)

MAX_WORKERS = 10
ROOT_URL = BASE_URL + '/brandenburgaktuell/landschleicher/'

BASE = sys.argv[0]
HANDLE = int(sys.argv[1])


def build_url(**params) -> str:
    return f'{BASE}?{urlencode(params)}'


def show_root() -> None:
    for label_id, action in ((strings.LATEST, 'neueste'), (strings.LANDKREISE, 'landkreise'), (strings.SEARCH, 'suche')):
        item = xbmcgui.ListItem(label=kodiutils.get_string(label_id))
        xbmcplugin.addDirectoryItem(HANDLE, build_url(action=action), item, True)
    xbmcplugin.endOfDirectory(HANDLE)


def show_landkreise() -> None:
    landkreise = parser.parse_landkreise(http.fetch(ROOT_URL))
    for landkreis in sorting.sortiere_landkreise(landkreise, kodiutils.get_setting_as_int('sort_landkreise')):
        item = xbmcgui.ListItem(label=landkreis.name)
        xbmcplugin.addDirectoryItem(HANDLE, build_url(action='landkreis', url=landkreis.url), item, True)
    xbmcplugin.endOfDirectory(HANDLE)


def fetch_details(dorf: Dorf):
    try:
        return dorf.url, parser.parse_meta(http.fetch_head(dorf.url))
    except OSError as e:
        logger.warning('Could not load details for %s: %s', dorf.url, e)
        return dorf.url, None


def sortierte_doerfer(doerfer):
    return sorting.sortiere_doerfer(doerfer, kodiutils.get_setting_as_int('sort_doerfer'))


def show_doerfer(doerfer, reload_url: str = '') -> None:
    cache = DetailCache()
    doerfer = [cache.apply(d) for d in doerfer]
    for dorf in doerfer:
        datum = parser.format_datum(dorf.datum)
        item = xbmcgui.ListItem(label=f'{dorf.name} ({datum})' if datum else dorf.name)
        tag = item.getVideoInfoTag()
        tag.setTitle(dorf.name)
        tag.setPlot(dorf.beschreibung)
        item.setProperty('IsPlayable', 'true')
        if dorf.bild:
            item.setArt({'thumb': dorf.bild, 'poster': dorf.bild})
        xbmcplugin.addDirectoryItem(HANDLE, build_url(action='play', url=dorf.url), item, False)
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)
    nachladen([d for d in doerfer if d.url not in cache], cache, BASE + sys.argv[2], reload_url)


def nachladen(fehlende, cache: DetailCache, folder_path: str, reload_url: str = '') -> None:
    """Loads missing details after the list is shown, then reloads the list if it is still open.

    reload_url replaces the current folder, for lists whose URL cannot be refreshed as is.
    """
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
    logger.debug('Loaded details for %d of %d entries', neu, len(fehlende))
    if neu:
        cache.save()
        if xbmc.getInfoLabel('Container.FolderPath') == folder_path:
            xbmc.executebuiltin(f'Container.Update({reload_url}, replace)' if reload_url else 'Container.Refresh')


def suche(text: str) -> None:
    reload_url = ''
    text = text.strip()
    if not text:
        text = xbmcgui.Dialog().input(kodiutils.get_string(strings.SEARCH)).strip()
        if not text:
            xbmcplugin.endOfDirectory(HANDLE, succeeded=False)
            return
        # The prompt URL has no query, so a plain refresh would ask again
        reload_url = build_url(action='suche', q=text)
    treffer = search.suche_doerfer(parser.parse_doerfer(http.fetch(ROOT_URL + 'a-z.html')), text)
    if not treffer:
        kodiutils.notification(kodiutils.get_string(strings.NO_RESULTS))
    show_doerfer(sortierte_doerfer(treffer), reload_url)


def run() -> None:
    kodilogging.config()
    params = dict(parse_qsl(sys.argv[2].lstrip('?')))
    action = params.get('action')
    try:
        if action is None:
            show_root()
        elif action == 'landkreise':
            show_landkreise()
        elif action == 'neueste':
            show_doerfer(parser.parse_neueste(http.fetch(ROOT_URL)))
        elif action == 'suche':
            suche(params.get('q', ''))
        elif action == 'landkreis' and params.get('url', '').startswith(ROOT_URL):
            show_doerfer(sortierte_doerfer(parser.parse_doerfer(http.fetch(params['url']))))
        elif action == 'play' and params.get('url', '').startswith(ROOT_URL):
            player.play(HANDLE, params['url'])
        elif action == 'clear_cache':
            DetailCache().clear()
            kodiutils.notification(kodiutils.get_string(strings.CACHE_CLEARED))
        else:
            xbmcplugin.endOfDirectory(HANDLE, succeeded=False)
    except OSError as e:
        logger.error('Request %s failed: %s', sys.argv[2], e)
        kodiutils.notification(str(e))
        xbmcplugin.endOfDirectory(HANDLE, succeeded=False)
