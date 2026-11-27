import re

# The slug in a Beitrag URL (.../beitraege/<slug>/...) is the same as on the Landkreis pages
NAMEN = {
    'prignitz': 'Prignitz',
    'ostprignitz-ruppin': 'Ostprignitz-Ruppin',
    'oberhavel': 'Oberhavel',
    'uckermark': 'Uckermark',
    'barnim': 'Barnim',
    'maerkisch-oderland': 'Märkisch-Oderland',
    'oder-spree': 'Oder-Spree',
    'spree-neisse': 'Spree-Neiße',
    'oberspreewald-lausitz': 'Oberspreewald-Lausitz',
    'elbe-elster': 'Elbe-Elster',
    'teltow-flaeming': 'Teltow-Fläming',
    'potsdam-mittelmark': 'Potsdam-Mittelmark',
    'havelland': 'Havelland',
    'dahme-spreewald': 'Dahme-Spreewald',
}

_SLUG_RE = re.compile(r'/beitraege/([^/]+)/')


def name_aus_url(url: str) -> str:
    """Returns the Landkreis name of a Beitrag URL, or '' for pages outside the Landkreise."""
    match = _SLUG_RE.search(url)
    return NAMEN.get(match.group(1), '') if match else ''
