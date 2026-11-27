import sys
from xbmcgui import ListItem
from xbmcplugin import setResolvedUrl


def videoUrlZumLink(link: str):
    if (str != ''):
        print('####################################Spiel Videooooo')
        return 'https://rbbhttpstream-a.akamaihd.net/rbb/aktuell/landschleicher/prignitz/aktuell_19990131_Gerdshagen_PR_m_16_9_512x288.mp4'


def spieleVideo(videoUrl) -> None:
    play_item = ListItem(path=videoUrl)
    play_item.setProperty('IsPlayable', 'true')
    setResolvedUrl(int(sys.argv[1]), True, listitem=play_item)
