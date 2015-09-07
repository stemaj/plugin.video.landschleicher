#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import re

def getUrl(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:19.0) Gecko/20100101 Firefox/19.0')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return link

rbbUrl = "http://www.rbb-online.de"
baseUrl = rbbUrl + "/brandenburgaktuell/landschleicher"
archivBase = baseUrl + "/archiv"
archivUrl = archivBase + ".html"
chronologischBase = baseUrl + "/chronologisch/index"
chronologischUrl = chronologischBase + ".html"

def getLetters():
    archivSite = getUrl(archivUrl)
    letters = re.compile("<a href=\"/brandenburgaktuell/landschleicher/archiv/(.+?).html\" title=\"(.+?)\"", re.DOTALL).findall(archivSite)
    return letters

def getYears():
    chronologischSite = getUrl(chronologischUrl)
    years = re.compile("<a href=\"/brandenburgaktuell/landschleicher/chronologisch/index/(.+?).html").findall(chronologischSite)
    return years

def getYearUrl(year):
    return chronologischBase + "/" + str(year) + ".html"

def getLetterUrl(letter,page):
    return archivBase + "/" + letter + ".htm/page=" + str(page-1) + ".html"

villages = []
villageDescriptions = []
villageLinks = []
villageImages = []

def setVillageContent(url):
    global villages
    global villageDescriptions
    global villageLinks
    global villageImages
    global hasNextSite
    global nextSite

    tSite = getUrl(url).split(r"Drei-Stufen")
    tSite2 = tSite[0].split("<!-- Default Content -->")
    
    villages = re.compile("manualteasertitle\">(.+?)</span>", re.DOTALL).findall(tSite2[1])
    
    villageDescriptions = re.compile("manualteasershorttext\">(.+?)</div>", re.DOTALL).findall(tSite2[1])
    for i in range(len(villageDescriptions)): 
        villageDescriptions[i] = villageDescriptions[i].replace("<p>","")
        villageDescriptions[i] = villageDescriptions[i].replace("</p>","")

    villageLinks = re.compile("'{}'><a href=\"/brandenburgaktuell/landschleicher(.+?)\" class=\"sendeplatz\"><img", re.DOTALL).findall(tSite2[1])

    villageImages = re.compile(" src=\"(.+?jpg)\"", re.DOTALL).findall(tSite2[1])

    thisSiteNr = re.compile("page=(.+?).html", re.DOTALL).findall(url)
    hasNextSite = False
    nextSite = ""
    if (len(thisSiteNr) > 0):
        nr = int(thisSiteNr[0]) + 1
        nextSiteNr = re.compile("page=" + str(nr) + ".html", re.DOTALL).findall(tSite2[1])
        if (len(nextSiteNr) > 0):
            hasNextSite = True
            nextSite = url.replace(str(nr-1),str(nr))


def getVillageVideoLink(url):
    villageSite = getUrl(url)
    
    jsnLink = re.compile("data-media-ref=\"(.+?jsn)\"", re.DOTALL).findall(villageSite)
    
    videoUrlSite = getUrl(rbbUrl + jsnLink[0])
    
    videoLink = re.compile("stream\":\"(.+?mp4)\"", re.DOTALL).findall(videoUrlSite)

    return videoLink[0]

# Test: 5. Dorf der 2. D-Seite 
#letters = getLetters()
#setVillageContent(getLetterUrl(letters[17][0],8))
#link = getVillageVideoLink(baseUrl + villageLinks[4])

#years = getYears()
#setVillageContent(getYearUrl(years[3]))
#link = getVillageVideoLink(baseUrl + villageLinks[4])

#i = 2

