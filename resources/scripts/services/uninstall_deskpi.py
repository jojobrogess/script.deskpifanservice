import os
import xbmc
import xbmcaddon

__addon__ = xbmcaddon.Addon('script.deskpifanservice')
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')
 
line1 = "All Deskpi Files and Services have been deleted.\n"
line2 = "You can now uninstall the addon."
time = 5000 #in miliseconds

os.system('cp /storage/.kodi/addons/script.deskpifanservice/resources/lib/uninstall_deskpi.sh /storage/')
os.system('sh /storage/uninstall_deskpi.sh')
xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1+line2, time, __icon__))
