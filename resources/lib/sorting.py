from typing import List

from resources.lib.models import Dorf, Landkreis

# Values of the "sort_landkreise" and "sort_doerfer" settings
NAME_AZ = 0
NAME_ZA = 1
DATUM_NEUESTE = 2
DATUM_AELTESTE = 3


def sortiere_landkreise(landkreise: List[Landkreis], modus: int) -> List[Landkreis]:
    return sorted(landkreise, key=lambda l: l.name.casefold(), reverse=modus == NAME_ZA)


def sortiere_doerfer(doerfer: List[Dorf], modus: int) -> List[Dorf]:
    if modus in (DATUM_NEUESTE, DATUM_AELTESTE):
        # datum is ISO formatted, so it sorts chronologically as text
        return sorted(doerfer, key=lambda d: d.datum, reverse=modus == DATUM_NEUESTE)
    return sorted(doerfer, key=lambda d: d.name.casefold(), reverse=modus == NAME_ZA)
