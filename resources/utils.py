import xbmc
import xbmcgui
import xbmcaddon


__addon_id__ = 'script.deskpifanservice'
__Addon = xbmcaddon.Addon(__addon_id__)
__icon__ = __Addon.getAddonInfo('icon')


def addon_dir():
    return __Addon.getAddonInfo('path')


def open_settings():
    __Addon.openSettings()


def get_string(string_id):
    return __Addon.getLocalizedString(string_id)


def log(message, loglevel=xbmc.LOGDEBUG):
    xbmc.log(__addon_id__ + "-" + __Addon.getAddonInfo('version') + ": " + message, level=loglevel)


def show_notification(message):
    xbmcgui.Dialog().notification(get_string(30000), message, time=5000, icon=__icon__)


def get_setting(name):
    return __Addon.getSetting(name)


def setsetting(name, value):
    __Addon.setSetting(name, value)
