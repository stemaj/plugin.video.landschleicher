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
villageDates = []

def setVillageContent(url):
    global villages
    global villageDescriptions
    global villageLinks
    global villageImages
    global villageDates
    global hasNextSite
    global nextSite

    tSite = getUrl(url).split(r"Drei-Stufen")
    tSite2 = tSite[0].split("<!-- Default Content -->")
    tSite3 = tSite2[1].split("<article")
    tSite3.pop(0)

    for fragment in tSite3:
        
        fvillages = re.compile("manualteasertitle\">(.+?)</span>", re.DOTALL).findall(fragment)
        
        fvillageDescriptions = re.compile("manualteasershorttext\">(.+?)</div>", re.DOTALL).findall(fragment)
        for i in range(len(fvillageDescriptions)): 
            fvillageDescriptions[i] = fvillageDescriptions[i].replace("<p>","")
            fvillageDescriptions[i] = fvillageDescriptions[i].replace("</p>","")

        fvillageLinks = re.compile("'{}'><a href=\"/brandenburgaktuell/landschleicher(.+?)\" class=\"sendeplatz\"><img", re.DOTALL).findall(fragment)

        fvillageImages = re.compile(" src=\"(.+?jpg)\"", re.DOTALL).findall(fragment)

        fvillageDate = re.compile("datetime=\"(.+?)T", re.DOTALL).findall(fragment)

        # hat gültigen Name und Link?
        if (len(fvillages) == 1 and len(fvillageLinks) == 1):
            villages.append(fvillages[0])
            villageLinks.append(fvillageLinks[0])

            # dazu ein gültiges Bild
            if (len(fvillageImages) == 1):
                villageImages.append(fvillageImages[0])
            else:
                villageImages.append("content/dam/rbb/rbb/logos/touch.png/_jcr_content/renditions/appletouchicon57x57precomposed.png")

            # dazu eine gültige Beschreibung
            if (len(fvillageDescriptions) == 1):
                villageDescriptions.append(fvillageDescriptions[0])
            else:
                villageDescriptions.append("")

            # dazu ein gültiges Datum
            if (len(fvillageDate) == 1):
                villageDates.append(fvillageDate[0])
            else:
                villageDates.append("")


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

# Test: 5. Dorf der 3. S-Seite 
#letters = getLetters()
#setVillageContent(getLetterUrl(letters[17][0],3))
#link = getVillageVideoLink(baseUrl + villageLinks[4])

#years = getYears()
#setVillageContent(getYearUrl(years[3]))
#link = getVillageVideoLink(baseUrl + villageLinks[4])

#i = 2

