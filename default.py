#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc
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
alphabetisch = addon.getSetting("sortierung") == "0"
videoquality = addon.getSetting("videoquality")

# resources
RES_naechsteSeite = "Nächste Seite"
RES_landschleicher = "Landschleicher"
RES_seiteNichtGelesen = "Die Seite konnte nicht gelesen werden."

def addDir(title, stream, thumb, mode):
    link = sys.argv[0]+"?url="+urllib.quote_plus(stream)+"&mode="+str(mode)
    liz = xbmcgui.ListItem(title, iconImage=None, thumbnailImage=thumb)
    liz.setInfo(type="Video", infoLabels={"Title": title})
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=link, listitem=liz, isFolder=True)

def addLink(name, url, mode, iconimage, label, date):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+urllib.quote_plus(mode)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": label, "Tagline": date})
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

def notification(text):
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(RES_landschleicher, text, 4500, icon))

def listLetters():
    global sortierungUmkehren
    sortierungUmkehren = False
    letters = landschleicherCore.getLetters()
    if not isinstance(letters,basestring):
        for letter in letters:
            addDir(letter[1], landschleicherCore.getLetterUrl(letter[0], 1), icon, 'listVideos')
        xbmcplugin.endOfDirectory(addon_handle)
    else:
        notification(letters)

def listYears():
    global sortierungUmkehren
    sortierungUmkehren = True
    years = landschleicherCore.getYears()
    if not isinstance(years,basestring):
        for year in years:
            addDir(year, landschleicherCore.getYearUrl(year), icon, 'listVideos')
        xbmcplugin.endOfDirectory(addon_handle)
    else:
        notification(years)

def listVideos(url, sortierungUmkehren):
    i = 0
    error = landschleicherCore.setVillageContent(url, sortierungUmkehren)
    if error:
        notification(error)
        return
    if (len(landschleicherCore.villages) == 0):
        notification(RES_seiteNichtGelesen)
        return
    for village in landschleicherCore.villages:
        addLink(village, landschleicherCore.baseUrl + landschleicherCore.villageLinks[i], 'playVideo', landschleicherCore.rbbUrl + landschleicherCore.villageImages[i], landschleicherCore.villageDescriptions[i], landschleicherCore.villageDates[i])
        i = i+1
    if (landschleicherCore.hasNextSite):
        addDir(RES_naechsteSeite, landschleicherCore.nextSite, icon, 'listVideos')
    xbmcplugin.endOfDirectory(addon_handle)

def playVideo(url):
    vLink = landschleicherCore.getVillageVideoLink(url, videoquality)
    if not vLink[0]:
        notification(vLink[1])
        return
    listitem = xbmcgui.ListItem(path=vLink[0])
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem)

if mode == "playVideo":
    playVideo(url)
elif mode == "listVideos":
    if (alphabetisch):
        listVideos(url, False)
    else:
        listVideos(url, True)
else:
    if (alphabetisch):
        listLetters()
    else:
        listYears()
