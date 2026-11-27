import xbmcgui
import xbmcplugin

from resources.lib.scraper import http, parser
from resources.lib.utils import kodiutils


def play(handle: int, url: str) -> None:
    try:
        video_url = parser.parse_video_url(http.fetch(url))
    except OSError as e:
        kodiutils.notification('Landschleicher', str(e))
        xbmcplugin.setResolvedUrl(handle, False, xbmcgui.ListItem())
        return
    if not video_url:
        kodiutils.notification('Landschleicher', 'Zu diesem Beitrag gibt es kein Video.')
        xbmcplugin.setResolvedUrl(handle, False, xbmcgui.ListItem())
        return
    xbmcplugin.setResolvedUrl(handle, True, xbmcgui.ListItem(path=video_url))
