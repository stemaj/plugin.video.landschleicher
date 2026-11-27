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
