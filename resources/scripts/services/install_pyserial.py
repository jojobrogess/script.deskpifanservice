import os
import xbmc
import xbmcaddon

__addon__ = xbmcaddon.Addon('script.deskpifanservice')
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')
 
line1 = "Pyserial Installer Has Started\n"
line2 = "Give it a couple second and then please continue on..."
time = 5000 #in miliseconds

os.system('cp /storage/.kodi/addons/script.deskpifanservice/resources/lib/pyserial_installer.sh /storage/')
os.system('sh /storage/pyserial_installer.sh')
xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1+line2, time, __icon__))
