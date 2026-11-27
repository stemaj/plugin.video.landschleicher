import logging

import xbmc
import xbmcaddon

from resources.lib.utils.kodiutils import get_setting_as_bool

LEVELS = {
    logging.CRITICAL: xbmc.LOGFATAL,
    logging.ERROR: xbmc.LOGERROR,
    logging.WARNING: xbmc.LOGWARNING,
    logging.INFO: xbmc.LOGINFO,
    logging.DEBUG: xbmc.LOGDEBUG,
}


class KodiLogHandler(logging.Handler):
    """Forwards Python log records to the Kodi log."""

    def __init__(self) -> None:
        super().__init__()
        addon_id = xbmcaddon.Addon().getAddonInfo('id')
        self.setFormatter(logging.Formatter(f'[{addon_id}] %(name)s: %(message)s'))

    def emit(self, record: logging.LogRecord) -> None:
        xbmc.log(self.format(record), LEVELS.get(record.levelno, xbmc.LOGDEBUG))


def config() -> None:
    root = logging.getLogger()
    if not any(isinstance(h, KodiLogHandler) for h in root.handlers):
        root.addHandler(KodiLogHandler())
    root.setLevel(logging.DEBUG if get_setting_as_bool('debug') else logging.INFO)
