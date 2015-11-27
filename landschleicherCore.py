#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import re
import httplib
#import socket

def getUrl(url):
    error = ''
    link = ''
    req = urllib2.Request(url, headers={'accept': '*/*'})
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:19.0) Gecko/20100101 Firefox/19.0')
    try:
        response = urllib2.urlopen(req)
        if not response:
            error = 'No response - Please try again'
    except urllib2.HTTPError as e:
        error = 'Error code: ', e.code
    except urllib2.URLError as e:
        error = 'Reason: ', e.reason
    except Exception as e:
        if e.message:
            error = e.message
        else:
            error = 'Other reason'
    if not error:
        try:
            link = response.read()
            if not link:
                error = 'No data - Please try again'
        except httplib.IncompleteRead as e:
            error = e.message
        except Exception as e:
            error = e.message
    
    if not error:
        if response:
            response.close()

    return (link, error)

#socket.setdefaulttimeout(5) # timeout in seconds
rbbUrl = "http://www.rbb-online.de"
baseUrl = rbbUrl + "/brandenburgaktuell/landschleicher"
archivBase = baseUrl + "/archiv"
archivUrl = archivBase + ".html"
chronologischBase = baseUrl + "/chronologisch/index"
chronologischUrl = chronologischBase + ".html"

def getLetters():
    archivSite = getUrl(archivUrl)
    error = archivSite[1]
    if not error:
        letters = re.compile("<a href=\"/brandenburgaktuell/landschleicher/archiv/(.+?).html\" title=\"(.+?)\"", re.DOTALL).findall(archivSite[0])
        if (len(letters) > 0):
            return letters
        else:
            error = 'Please try again'
    return error

def getYears():
    chronologischSite = getUrl(chronologischUrl)
    error = chronologischSite[1]
    if not error:
        years = re.compile(".html\" title=\"([0-9]+?)\"").findall(chronologischSite[0])
        if (len(years) > 0):
            return years
        else:
            error = 'Please try again'
    return error

def getYearUrl(year):
    return chronologischBase + "/" + str(year) + ".html"

def getLetterUrl(letter,page):
    return archivBase + "/" + letter + ".htm/page=" + str(page-1) + ".html"

villages = []
villageDescriptions = []
villageLinks = []
villageImages = []
villageDates = []

def setVillageContent(url, sortierungUmkehren = False):
    global villages
    global villageDescriptions
    global villageLinks
    global villageImages
    global villageDates
    global hasNextSite
    global nextSite

    site = getUrl(url)
    if not site[0]:
        return site[1]
    
    tSite = site[0].split(r"Drei-Stufen")
    tSite2 = tSite[0].split("<!-- Default Content -->")
    
    if (len(tSite2) < 2):
        return 'Parse Error'

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

    if sortierungUmkehren:
        villages.reverse()
        villageLinks.reverse()
        villageImages.reverse()
        villageDescriptions.reverse()
        villageDates.reverse()
                
    thisSiteNr = re.compile("page=(.+?).html", re.DOTALL).findall(url)
    hasNextSite = False
    nextSite = ""
    if (len(thisSiteNr) > 0):
        nr = int(thisSiteNr[0]) + 1
        nextSiteNr = re.compile("page=" + str(nr) + ".html", re.DOTALL).findall(tSite2[1])
        if (len(nextSiteNr) > 0):
            hasNextSite = True
            nextSite = url.replace(str(nr-1),str(nr))

    return ''

def getVillageVideoLink(url, quality):
    
    error = ''
    villageSite = getUrl(url)
    if not villageSite[0]:
        return (villageSite[0], villageSite[1])

    jsnLink = re.compile("data-media-ref=\"(.+?jsn)\"", re.DOTALL).findall(villageSite[0])
    
    if (len(jsnLink) == 0):
        return ('', 'Video Link Parse Error')

    videoUrlSite = getUrl(rbbUrl + jsnLink[0])
    if not videoUrlSite[0]:
        return (videoUrlSite[0],videoUrlSite[1])
    
    videoLink = re.compile("stream\":\"(.+?mp4)\"", re.DOTALL).findall(videoUrlSite[0])
    videoquality = re.compile("_quality\":([0-9])}", re.DOTALL).findall(videoUrlSite[0])

    if (str(quality) in videoquality):
        index = videoquality.index(str(quality))
    else:
        index = 0

    return (videoLink[index], error)

## Test: 5. Dorf der 3. S-Seite 
#letters = getLetters()
#if not isinstance(letters,basestring):
#    error = setVillageContent(getLetterUrl(letters[17][0],3))
#    if not error:
#        link = getVillageVideoLink(baseUrl + villageLinks[4], 3)
#        print link
#    else:
#        print error
#else:
#    print letters

## Test: 5. Dorf des 3. Jahres
#years = getYears()
#if not isinstance(years,basestring):
#    error = setVillageContent(getYearUrl(years[0]), True)
#    if not error:
#        link = getVillageVideoLink(baseUrl + villageLinks[2], 2)
#        print link
#    else:
#        print error
#else:
#    print years

#i = 2
