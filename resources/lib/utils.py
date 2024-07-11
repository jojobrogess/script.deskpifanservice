import xbmc
import xbmcvfs
import xbmcgui
import xbmcaddon

__addon_id__ = 'script.deskpifanservice'
__addon = xbmcaddon.Addon(__addon_id__)
__icon__ = __addon.getAddonInfo('icon')

LOG_LEVELS = {
    "DEBUG": xbmc.LOGDEBUG,
    "INFO": xbmc.LOGINFO,
    "WARNING": xbmc.LOGWARNING,
    "ERROR": xbmc.LOGERROR,
    "FATAL": xbmc.LOGFATAL
}


def translate_path(path):
    return xbmcvfs.translatePath(path)


# output *libre = /storage/.kodi/addons/script.deskpifanservice/
# output *osmc = /home/osmc/.kodi/addons/script.deskpifanservice/
def addon_dir():
    return translate_path(__addon.getAddonInfo('path'))


# output = /storage/.kodi/userdata/addon_data/script.deskpifanservice/
# output *osmc = /home/osmc/.kodi/addon_data/script.deskpifanservice/
def addon_data_dir():
    addon_data_path = translate_path('special://userdata/addon_data/' + __addon_id__)
    return addon_data_path


def get_string(string_id):
    return __addon.getLocalizedString(string_id)


def get_setting(name):
    return __addon.getSetting(name)


def open_settings():
    __addon.openSettings()


# string 30000 is 'script.deskpifanservice'
def show_notification(message):
    xbmcgui.Dialog().notification(get_string(30000), message, time=5000, icon=__icon__)


def show_dialog(message):
    xbmcgui.Dialog().ok(get_string(30000), message)


# Usage = log(file_name, "message")
def log(source_file=None, message=None, loglevel="DEBUG"):
    loglevel = LOG_LEVELS.get(loglevel, xbmc.LOGINFO)
    xbmc.log(f"While running {source_file}: {message}", level=loglevel)
