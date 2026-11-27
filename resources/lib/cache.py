import json
import os
from dataclasses import replace
from typing import Dict

import xbmcaddon
import xbmcvfs

from resources.lib.models import Dorf


class DetailCache:
    """Persists description and image per Beitrag URL in the addon profile."""

    def __init__(self) -> None:
        profile = xbmcvfs.translatePath(xbmcaddon.Addon().getAddonInfo('profile'))
        xbmcvfs.mkdirs(profile)
        self._path = os.path.join(profile, 'details.json')
        self._data: Dict[str, Dict[str, str]] = self._load()
        self._new: Dict[str, Dict[str, str]] = {}

    def _load(self) -> Dict[str, Dict[str, str]]:
        try:
            with open(self._path, encoding='utf-8') as f:
                return json.load(f)
        except (OSError, ValueError):
            return {}

    def __contains__(self, url: str) -> bool:
        return url in self._data

    def apply(self, dorf: Dorf) -> Dorf:
        entry = self._data.get(dorf.url)
        if not entry:
            return dorf
        return replace(dorf, beschreibung=entry.get('beschreibung', ''), bild=entry.get('bild', ''))

    def put(self, url: str, beschreibung: str, bild: str) -> None:
        self._data[url] = self._new[url] = {'beschreibung': beschreibung, 'bild': bild}

    def clear(self) -> None:
        self._data = {}
        self._new = {}
        try:
            os.remove(self._path)
        except OSError:
            pass

    def save(self) -> None:
        # Merge with the file again, since another list may have saved entries in the meantime
        merged = {**self._load(), **self._new}
        tmp = self._path + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(merged, f, ensure_ascii=False)
        os.replace(tmp, self._path)
