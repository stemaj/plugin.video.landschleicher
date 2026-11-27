from typing import List

from resources.lib.models import Dorf


def suche_doerfer(doerfer: List[Dorf], text: str) -> List[Dorf]:
    """Case-insensitive substring match on the village name; ignores non-Beitrag pages like templates."""
    begriff = text.strip().casefold()
    return [d for d in doerfer
            if begriff in d.name.casefold() and '/beitraege/' in d.url and '/vorlagen' not in d.url]
