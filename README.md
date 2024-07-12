# script.deskpifanservice
## Libreelec Addon to install Deskpi Fan Service and Control Fan Speed.
### You MUST be on at least `LibreELEC-RPi4.arm-9.95.4` or `OSMC December 10, 2023`

**********************************************************************************************************************************************************************
### PRIOR TO USAGE, GO TO: Settings > Installation > Install
### PLEASE REBOOT AFTER INSTALLING DESKPI SERVICE.

*Remember to press `OK` to set the settings, if you back out they will not be applied.

*Installation requires modification to flash/config.txt file to add the flags:

`otg_mode=1`, `dtoverlay=dwc2`, `dr_mode=host`, `dtoverlay=gpio-ir`, `gpio_pin=17`

*Installation uses HARDCODED TTY/USB0 SERIAL Device, if you have complications let me know. 
**********************************************************************************************************************************************************************
**********************************************************************************************************************************************************************

Kodi File Manager Repository Source:
https://jojobrogess.github.io/repository.deskpi/
