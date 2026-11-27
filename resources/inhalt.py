import sys
from xbmcplugin import setResolvedUrl
from xbmcgui import ListItem

class Landschleicher():
    beitraege = {}
    @staticmethod
    def addLandkreis(x):
        Landschleicher.beitraege[x] = []
    @staticmethod
    def addBeitrag(x,y):
        Landschleicher.beitraege[x].append(y)

class Film():
    def __init__(self, film: str, link: str, datetime: str):
        self.film = film
        self.link = link
        self.datetime = datetime

def listeDerNeuestenFilme():
    a = Film('film1', "link1", 'Bla')
    b = Film('film2', "link2", 'Bla')
    arr = []
    arr.append(a)
    arr.append(b)
    return arr

def videoUrlZumLink(link: str):
    if (str != ''):
        print('####################################Spiel Videooooo')
        return 'https://rbbhttpstream-a.akamaihd.net/rbb/aktuell/landschleicher/prignitz/aktuell_19990131_Gerdshagen_PR_m_16_9_512x288.mp4'

def spieleVideo(videoUrl) -> None:
    play_item = ListItem(path=videoUrl)
    play_item.setProperty('IsPlayable', 'true')
    setResolvedUrl(int(sys.argv[1]), True, listitem=play_item)
