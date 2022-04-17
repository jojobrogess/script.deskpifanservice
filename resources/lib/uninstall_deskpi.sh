#!/bin/bash
daemonname="deskpi"
################################################################
################## START UNINSTALLATION SCRIPT ###################
################################################################

cd ~/

systemctl disable $daemonname-default.service 2&>/dev/null
systemctl stop $daemonname-default.service  2&>/dev/null
systemctl disable $daemonname-poweroff.service 2&>/dev/null
systemctl stop $daemonname-poweroff.service 2&>/dev/null

rm -f  /storage/.config/system.d/$daemonname-poweroff.service 2&>/dev/null
rm -f  /storage/.config/system.d/$daemonname-default.service  2&>/dev/null
rm -f /storage/user/bin/$daemonname-fancontrol.py 2&>/dev/null
rm -f /storage/user/bin/$daemonname-poweroff.py 2&>/dev/null
rm -f /storage/user/bin/$daemonname.conf 2&>/dev/null
rm -f /storage/user/bin/$daemonname.conf

rm -- "$0"
