import os
import xbmc
import xbmcaddon
import xbmcgui

__addon__ = xbmcaddon.Addon('script.deskpifanservice')
__addonname__ = __addon__.getAddonInfo('name')

line1 = "If your device does not reboot. Please reboot your device.\n"
line2 = "\n"
line3 = "Then return to the settings page to finish setting everything up."

os.system('cp /storage/.kodi/addons/script.deskpifanservice/resources/lib/deskpi_installer.sh /storage/')
os.system('sh /storage/deskpi_installer.sh')
xbmcgui.Dialog().ok(__addonname__, line1+line2+line3)
