import json
import logging

import xbmc
import xbmcaddon
import xbmcgui

logger = logging.getLogger(__name__)


def _addon() -> xbmcaddon.Addon:
    return xbmcaddon.Addon()


def notification(header: str, message: str, time: int = 5000, icon: str = '', sound: bool = True) -> None:
    icon = icon or _addon().getAddonInfo('icon')
    xbmcgui.Dialog().notification(header, message, icon, time, sound)


def show_settings() -> None:
    _addon().openSettings()


def get_setting(setting: str) -> str:
    return _addon().getSettingString(setting)


def get_setting_as_bool(setting: str) -> bool:
    return _addon().getSettingBool(setting)


def get_setting_as_int(setting: str) -> int:
    return _addon().getSettingInt(setting)


def get_setting_as_float(setting: str) -> float:
    return _addon().getSettingNumber(setting)


def set_setting(setting: str, value) -> None:
    _addon().setSetting(setting, str(value))


def get_string(string_id: int) -> str:
    return _addon().getLocalizedString(string_id)


def kodi_json_request(params: dict):
    response = json.loads(xbmc.executeJSONRPC(json.dumps(params)))
    if 'error' in response:
        logger.warning('[%s] %s', params.get('method'), response['error'].get('message'))
        return None
    return response.get('result')
