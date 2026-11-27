import logging

import xbmcgui
import xbmcplugin

from resources.lib import strings
from resources.lib.scraper import http, parser
from resources.lib.utils import kodiutils

logger = logging.getLogger(__name__)


def play(handle: int, url: str) -> None:
    try:
        video_url = parser.parse_video_url(http.fetch(url))
    except OSError as e:
        logger.error('Could not load %s: %s', url, e)
        kodiutils.notification(str(e))
        video_url = ''
    else:
        if not video_url:
            logger.warning('No video found on %s', url)
            kodiutils.notification(kodiutils.get_string(strings.NO_VIDEO))
    if not video_url:
        xbmcplugin.setResolvedUrl(handle, False, xbmcgui.ListItem())
        return
    logger.debug('Playing %s', video_url)
    xbmcplugin.setResolvedUrl(handle, True, xbmcgui.ListItem(path=video_url))
