# -*- coding: utf-8 -*-

import sys
import logging
import xbmcaddon
from resources.lib.utils import kodilogging
from xbmcplugin import endOfDirectory

ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()

def run():
    endOfDirectory(int(sys.argv[1]))
