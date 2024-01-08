# script.deskpifanservice
## Libreelec Addon to install Deskpi Fan Service and Control Fan Speed.
### You MUST be on at least `LibreELEC-RPi4.arm-9.95.4`.

**********************************************************************************************************************************************************************
### PRIOR TO USAGE, GO TO: Settings > Installation > Install
### PLEASE REBOOT AFTER INSTALLING DESKPI SERVICE.


*Installation requires modification to flash/config.txt file to add the flags:

`otg_mode=1`, `dtoverlay=dwc2`, `dr_mode=host`, `dtoverlay=gpio-ir`, `gpio_pin=17`

