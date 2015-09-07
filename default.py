#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmcaddon
import xbmcgui
import xbmcplugin
import urllib
import os.path
import landschleicherCore

#import ptvsd
#ptvsd.enable_attach(secret = 'm')
#ptvsd.wait_for_attach()

addonID = 'plugin.video.landschleicher'
addon = xbmcaddon.Addon(id=addonID)
addon_handle = int(sys.argv[1])
addonDir = xbmc.translatePath(addon.getAddonInfo('path'))
icon = os.path.join(addonDir ,'fanart.jpg')
xbmcplugin.setContent(addon_handle, "movies")
path = os.path.dirname(os.path.realpath(__file__))
addonID = os.path.basename(path)
addon = xbmcaddon.Addon(id=addonID)

def addDir(title, stream, thumb, mode):
    link = sys.argv[0]+"?url="+urllib.quote_plus(stream)+"&mode="+str(mode)
    liz = xbmcgui.ListItem(title, iconImage=None, thumbnailImage=thumb)
    liz.setInfo(type="Video", infoLabels={"Title": title})
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=link, listitem=liz, isFolder=True)

def addLink(name, url, mode, iconimage, label):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+urllib.quote_plus(mode)
    ok = True
    liz = xbmcgui.ListItem(name, label, iconImage=icon, thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    liz.setProperty("fanart_image", icon)
    liz.setProperty('IsPlayable', 'true')
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
    return ok

def parameters_string_to_dict(parameters):
	paramDict = {}
	if parameters:
		paramPairs = parameters[1:].split("&")
		for paramsPair in paramPairs:
			paramSplits = paramsPair.split('=')
			if (len(paramSplits)) == 2:
				paramDict[paramSplits[0]] = paramSplits[1]
	return paramDict

params = parameters_string_to_dict(sys.argv[2])
mode = urllib.unquote_plus(params.get('mode', ''))
url = urllib.unquote_plus(params.get('url', ''))
name = urllib.unquote_plus(params.get('name', ''))

def index():
    addDir('A-Z', landschleicherCore.archivUrl, icon, 'listLetters')
    addDir('Chronologisch', landschleicherCore.chronologischUrl, icon, 'listYears')
    xbmcplugin.endOfDirectory(addon_handle)

def listLetters():
    letters = landschleicherCore.getLetters()
    for letter in letters:
        addDir(letter[1], landschleicherCore.getLetterUrl(letter[0], 1), icon, 'listVideos')
    xbmcplugin.endOfDirectory(addon_handle)

def listYears():
    years = landschleicherCore.getYears()
    for year in years:
        addDir(year, landschleicherCore.getYearUrl(year), icon, 'listVideos')
    xbmcplugin.endOfDirectory(addon_handle)

def listVideos(url):
    i = 0
    landschleicherCore.setVillageContent(url)
    for village in landschleicherCore.villages:
        addLink(village, landschleicherCore.baseUrl + landschleicherCore.villageLinks[i], 'playVideo', landschleicherCore.rbbUrl + landschleicherCore.villageImages[i], landschleicherCore.villageDescriptions[i])
        i = i+1
    if (landschleicherCore.hasNextSite):
        addDir("Nächste Seite", landschleicherCore.nextSite, icon, 'listVideos')
    xbmcplugin.endOfDirectory(addon_handle)

def playVideo(url):
    vLink = landschleicherCore.getVillageVideoLink(url)
    listitem = xbmcgui.ListItem(path=vLink)
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem)

if mode == "playVideo":
    playVideo(url)
elif mode == "listVideos":
    listVideos(url)
elif mode == "listLetters":
    listLetters()
elif mode == "listYears":
    listYears()
else:
    index()
