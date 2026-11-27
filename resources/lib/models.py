from dataclasses import dataclass


@dataclass(frozen=True)
class Landkreis:
    slug: str
    name: str
    url: str


@dataclass(frozen=True)
class Dorf:
    name: str
    url: str
    datum: str
    beschreibung: str = ''
    bild: str = ''
