import routing
from xbmcplugin import addDirectoryItem, endOfDirectory, setResolvedUrl
from xbmcgui import ListItem
from pyStemaj import byteStream, bytesExtractor, stringExtractor

plugin = routing.Plugin()

class Film():
    def __init__(self, film: str, link: str, plot: str, poster: str):
        self.film = film
        self.link = link
        self.plot = plot
        self.poster = poster

def listeDerLandkreiseByData(listOfRawData: bytes):
    landkreisList = []
    for data in listOfRawData:
        # name = stringExtractor.matchByRegex(data, b"manualteasertitle\">(.+)</span")
        # link = stringExtractor.matchByRegex(data, b"href=\"(.+)\".class.+sendeplatz")
        # datetime = stringExtractor.matchByRegex(data, b"datetime.+>(.+)<")
        landkreis = stringExtractor.matchByRegex(bytes(data), b"beitraege/(.+)/.+html")
        if not landkreis in landkreisList:
            print(landkreis)
            if isinstance(landkreis, str):
                landkreisList.append(landkreis)
    return landkreisList

def listeDerLandkreise():
    return listeDerLandkreiseByData(byteStream.fromUrl("https://www.rbb-online.de/brandenburgaktuell/landschleicher/a-z.html"))

def listeDerLandkreisFilme(landkreis: str):
    a = Film('filmx', "link1", 'Bla', 'image1.jpg')
    b = Film('filmy', "link2", 'Bla', 'image2.jpg')
    arr = []
    arr.append(a)
    arr.append(b)
    return arr

def listeDerNeuestenFilme():
    a = Film('film1', "link1", 'Bla', 'image1.jpg')
    b = Film('film2', "link2", 'Bla', 'image2.jpg')
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
