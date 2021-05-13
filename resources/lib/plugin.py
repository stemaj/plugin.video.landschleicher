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
from resources import inhalt
from pyStemaj import kodiZeug

ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()
plugin = routing.Plugin()

def fuelleGuiMitListeVonLandkreisen(arr) -> None:
    for x in arr:
        addDirectoryItem(plugin.handle, plugin.url_for(show_landkreis, x)   , ListItem(x), True)
    endOfDirectory(plugin.handle)

def fuelleGuiMitListeVonFilmen(arr) -> None:
    for x in arr:
        listItem = ListItem(label=x.film)
        listItem.setArt({'poster':x.poster})
        listItem.setInfo('video',infoLabels={ 'plot': x.plot })
        listItem.setProperty('IsPlayable', 'true')
        addDirectoryItem(plugin.handle, plugin.url_for(play_video, x.link), listItem)
    endOfDirectory(plugin.handle)

@plugin.route('/')
def index():
    addDirectoryItem(plugin.handle, plugin.url_for(show_category, 'kategorieNeueste')   , ListItem('Neueste Videos'), True)
    addDirectoryItem(plugin.handle, plugin.url_for(show_category, 'kategorieAz')        , ListItem('A-Z')           , True)
    addDirectoryItem(plugin.handle, plugin.url_for(show_category, 'kategorieSuche')     , ListItem('Suche')         , True)
    endOfDirectory(plugin.handle)

@plugin.route('/category/<category_id>')
def show_category(category_id: str):
    if category_id == 'kategorieNeueste':
        fuelleGuiMitListeVonFilmen(inhalt.listeDerNeuestenFilme())
    elif category_id == 'kategorieAz':
        fuelleGuiMitListeVonLandkreisen(inhalt.listeDerLandkreise())
    elif category_id == 'kategorieSuche':
        text = kodiZeug.tastaturEingabe()
        if text:
            fuelleGuiMitListeVonFilmen(inhalt.listeDerNeuestenFilme())
        else:
            endOfDirectory(plugin.handle)

@plugin.route('/landkreis/<landkreis_id>')
def show_landkreis(landkreis_id: str):
    fuelleGuiMitListeVonFilmen(inhalt.listeDerLandkreisFilme(landkreis_id))


@plugin.route('/video/<video_id>')
def play_video(video_id):
    inhalt.spieleVideo(inhalt.videoUrlZumLink('nllll'))

def run():
    plugin.run()
