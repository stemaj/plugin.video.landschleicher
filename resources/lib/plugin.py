# -*- coding: utf-8 -*-

import routing
import logging
import xbmcaddon
from resources.lib import kodiutils
from resources.lib import kodilogging
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory
from xbmc import log
from resources.lib import main
from resources.lib import read


ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()
plugin = routing.Plugin()


@plugin.route('/')
def index():
    addDirectoryItem(plugin.handle, plugin.url_for(
        show_category, "one"), ListItem("Neueste"), True)
    endOfDirectory(plugin.handle)

@plugin.route('/category/<category_id>')
def show_category(category_id):
    if category_id == "one":
        data = read.load_url("https://www.rbb-online.de/brandenburgaktuell/landschleicher/chronologisch/index.htm/page=0.html")
        arr = main.listOfNewest(data, 13)
        for x in arr:
            data2 = read.load_url(x.link)
            data3 = main.videoLink(data2)
            log('#####LINK####' + data3 + '#####LINK####')
            listItem = ListItem(path=data3, label=x.film)
            listItem.setArt({'poster':x.poster})
            listItem.setInfo('video',infoLabels={ 'plot': x.plot })
            listItem.setProperty('IsPlayable', 'true')
            addDirectoryItem(plugin.handle, data3, listItem)
        endOfDirectory(plugin.handle)

def run():
    plugin.run()
