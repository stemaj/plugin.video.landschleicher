import xbmcaddon
import xbmcgui


def _addon() -> xbmcaddon.Addon:
    return xbmcaddon.Addon()


def notification(message: str, header: str = 'Landschleicher', time: int = 5000) -> None:
    xbmcgui.Dialog().notification(header, message, _addon().getAddonInfo('icon'), time)


def get_setting_as_bool(setting: str) -> bool:
    return _addon().getSettingBool(setting)


def get_setting_as_int(setting: str) -> int:
    return _addon().getSettingInt(setting)


def get_string(string_id: int) -> str:
    return _addon().getLocalizedString(string_id)
