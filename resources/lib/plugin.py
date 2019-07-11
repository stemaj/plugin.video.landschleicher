# -*- coding: utf-8 -*-

import routing
import logging
import xbmcaddon
from resources.lib import kodiutils
from resources.lib import kodilogging
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory, setResolvedUrl
from xbmc import log, Keyboard
from resources.lib import main
from resources.lib import read


ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()
plugin = routing.Plugin()


@plugin.route('/')
def index():
    addDirectoryItem(plugin.handle, plugin.url_for(show_category, "one"), ListItem("Neueste"), True)
    addDirectoryItem(plugin.handle, plugin.url_for(show_category, "two"), ListItem("Suche (ein Wort)"), True)
    endOfDirectory(plugin.handle)

@plugin.route('/category/<category_id>')
def show_category(category_id):
    if category_id == "one":
        data = read.load_url("https://www.rbb-online.de/brandenburgaktuell/landschleicher/chronologisch/index.htm/page=0.html")
        arr = main.listOfNewest(data)
        for x in arr:
            listItem = ListItem(label=x.film)
            repl = x.link.replace('/','~')
            log('#####REPL####' + repl + '#####REPL####')
            listItem.setArt({'poster':x.poster})
            listItem.setInfo('video',infoLabels={ 'plot': x.plot })
            listItem.setProperty('IsPlayable', 'true')
            addDirectoryItem(plugin.handle, plugin.url_for(play_video, repl), listItem)
        endOfDirectory(plugin.handle)
    elif category_id == "two":
        keyb = Keyboard()
        keyb.doModal()
        if keyb.isConfirmed():
            inp = keyb.getText()
            data = read.load_url("https://www.rbb-online.de/brandenburgaktuell/landschleicher/archiv.html#searchform_q__" + inp)
            arr = main.listOfNewest(data)
            for x in arr:
                listItem = ListItem(label=x.film)
                repl = x.link.replace('/','~')
                log('#####REPL####' + repl + '#####REPL####')
                listItem.setArt({'poster':x.poster})
                listItem.setInfo('video',infoLabels={ 'plot': x.plot })
                listItem.setProperty('IsPlayable', 'true')
                addDirectoryItem(plugin.handle, plugin.url_for(play_video, repl), listItem)
            endOfDirectory(plugin.handle)

@plugin.route('/video/<video_id>')
def play_video(video_id):
    video_url = video_id.replace('~','/')
    data2 = read.load_url(video_url)
    link = main.videoLink(data2)
    log('#####LINK####' + link + '#####LINK####')
    play_item = ListItem(path=link)
    play_item.setProperty('IsPlayable', 'true')
    setResolvedUrl(plugin.handle, True, listitem=play_item)

def run():
    plugin.run()
