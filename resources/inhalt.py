import routing
from xbmcplugin import addDirectoryItem, endOfDirectory, setResolvedUrl
from xbmcgui import ListItem
from xbmc import log
from pyStemaj import byteStream, bytesExtractor, stringExtractor

plugin = routing.Plugin()

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

def listeDerLandkreiseByData(arr):
    for data in arr:
        if isinstance(data, bytes):
            film = stringExtractor.matchByRegex(data, b"manualteasertitle\">(.+)</span")
            link = stringExtractor.matchByRegex(data, b"href=\"(.+)\".class.+sendeplatz")
            datetime = stringExtractor.matchByRegex(data, b"datetime.+>(.+)<")
            landkreis = stringExtractor.matchByRegex(bytes(data), b"beitraege/(.+)/.+html")
            if not landkreis in Landschleicher.beitraege and isinstance(landkreis, str):
                Landschleicher.addLandkreis(landkreis)
            if isinstance(landkreis, str):
                Landschleicher.addBeitrag(landkreis, Film(film,link,datetime))

def listeDerLandkreise():
    listeDerLandkreiseByData(bytesExtractor.extractInnerPartAndSplit(byteStream.fromUrl("https://www.rbb-online.de/brandenburgaktuell/landschleicher/a-z.html"), b"tab_content", b"commentSaved", b"</article>"))

def listeDerLandkreisFilme(landkreis: str):
    listeDerLandkreise()
    arr = []
    for x in Landschleicher.beitraege[landkreis]:
        arr.append(x)
    return arr

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
    setResolvedUrl(plugin.handle, True, listitem=play_item)
