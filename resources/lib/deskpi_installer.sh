#!/bin/bash
################################################################
################################################################
########## Deskpi Fan And Power Button Install Script ##########
################################################################
################################################################
daemonname="deskpi"
userlibrary=/storage/user/
defaultdriver=/storage/user/bin/$daemonname-defaultcontrol.py
daemonfanservice=/storage/.config/system.d/$daemonname-default.service
powerbutton=/storage/user/bin/$daemonname-poweroff.py
daemonspowerervice=/storage/.config/system.d/$daemonname-poweroff.service
################################################################
################## START INSTALLATION SCRIPT ###################
################################################################

echo "---------------------------------------------------------------"
echo "---------------------------------------------------------------"
echo "------------------- START INSTALL SCRIPT ----------------------"
echo "---------------------------------------------------------------"
echo "---------------------------------------------------------------"

############################
####### Script Create ######
############################


deskpi_create_file() {
	if [ -f $1 ]; then
        rm $1
    fi
	touch $1
}

############################
#Create User Lib/Bin Directory
############################

echo "DeskPi Fan control script installation Start."

if [ ! -d "/storage/user" ] ; then
	mkdir -p $userlibrary/bin
fi

############################
######Check Boot Mode######
############################

echo "Check Boot Mode"

PIINFO=$(cat /flash/config.txt | grep 'otg_mode=1,dtoverlay=dwc2,dr_mode=host,dtoverlay=gpio-ir,gpio_pin=17')
if [ -z "$PIINFO" ]
then
	mount -o remount,rw /flash
	echo "otg_mode=1,dtoverlay=dwc2,dr_mode=host,dtoverlay=gpio-ir,gpio_pin=17" >> /flash/config.txt
	mount -o remount,ro /flash
fi

echo "Successfully Checked and Created the Boot Mode"


#############################
#Create Default Driver Daemon
#############################

echo "Create Fan Default Driver Daemon"

deskpi_create_file $defaultdriver

echo 'import sys' >> $defaultdriver
echo "sys.path.append('/storage/.local/lib/python3.8/site-packages/')" >> $defaultdriver
echo 'import serial as serial' >> $defaultdriver
echo 'import time' >> $defaultdriver
echo 'import subprocess' >> $defaultdriver
echo '' >>$defaultdriver
echo "port = '/dev/ttyUSB0'" >>$defaultdriver
echo "baudrate = '9600'" >>$defaultdriver
echo 'ser = serial.Serial(port, baudrate, timeout=30)' >>$defaultdriver
echo '' >>$defaultdriver
echo 'try:' >> $defaultdriver
echo '    while True:' >> $defaultdriver
echo '        if ser.isOpen():' >> $defaultdriver
echo "            cpu_temp = subprocess.getoutput('vcgencmd measure_temp|awk -F\'=\' \'{print \$2\'}')" >> $defaultdriver
echo "            cpu_temp=int(cpu_temp.split('.')[0])" >> $defaultdriver
echo '' >>$defaultdriver
echo '            if cpu_temp < 35:' >> $defaultdriver
echo "                ser.write(b'pwm_000')" >> $defaultdriver
echo '            elif cpu_temp > 35 and cpu_temp < 40:' >> $defaultdriver
echo "                ser.write(b'pwm_025')" >> $defaultdriver
echo '            elif cpu_temp > 40 and cpu_temp < 45:' >> $defaultdriver
echo "                ser.write(b'pwm_0050')" >> $defaultdriver
echo '            elif cpu_temp > 45 and cpu_temp < 50:' >> $defaultdriver
echo "                ser.write(b'pwm_075')" >> $defaultdriver
echo '            elif cpu_temp > 50:' >> $defaultdriver
echo "                ser.write(b'pwm_100')" >> $defaultdriver
echo '' >>$defaultdriver
echo 'except KeyboardInterrupt:' >> $defaultdriver
echo "    ser.write(b'pwm_000')" >> $defaultdriver
echo '    ser.close()' >> $defaultdriver
echo ' ' >> $defaultdriver

chmod 755 $defaultdriver

echo "Successfully Created Default Driver Daemon"

############################
##Build Default Fan Service#
############################

echo "Building Fan Service"

deskpi_create_file $daemonfanservice

echo '[Unit]' >> $daemonfanservice
echo 'Description=DeskPi_Fan_Service' >> $daemonfanservice
echo 'After=multi-user.target' >> $daemonfanservice
echo '[Service]' >> $daemonfanservice
echo 'Type=simple' >> $daemonfanservice
echo 'RemainAfterExit=no' >> $daemonfanservice
echo 'ExecStart=/bin/sh -c ". /etc/profile; exec /usr/bin/python /storage/user/bin/deskpi-defaultcontrol.py"' >> $daemonfanservice
echo '[Install]' >> $daemonfanservice
echo 'WantedBy=multi-user.target' >> $daemonfanservice

chmod 644 $daemonfanservice

echo "Successfully Built Fan Service"

############################
#####Create Power Button####
############################

echo "Create Power Button Driver"

deskpi_create_file $powerbutton

echo 'import serial' >> $powerbutton
echo 'import time' >> $powerbutton
echo '' >> $powerbutton
echo 'ser=serial.Serial("/dev/ttyUSB0", 9600, timeout=30)' >> $powerbutton
echo '' >> $powerbutton
echo 'try: ' >> $powerbutton
echo '    while True:' >> $powerbutton
echo '        if ser.isOpen():' >> $powerbutton
echo "            ser.write(b'power_off')" >> $powerbutton
echo '            ser.close()' >> $powerbutton
echo '' >> $powerbutton
echo 'except KeyboardInterrupt:' >> $powerbutton
echo "    ser.write(b'power_off')" >> $powerbutton
echo '    ser.close()' >> $powerbutton
echo '    ' >> $powerbutton

chmod 755 $powerbutton

echo "Successfully Created Power Button Driver"

############################
#####Build Power Service####
############################

echo "Building Power Daemon"

deskpi_create_file $daemonspowerervice

echo '[Unit]' >> $daemonspowerervice
echo 'Description=DeskPi_Power_Button_Service' >> $daemonspowerervice
echo 'Conflicts=reboot.target' >> $daemonspowerervice
echo 'Before=halt.target shutdown.target poweroff.target' >> $daemonspowerervice
echo 'DefaultDependencies=no' >> $daemonspowerervice
echo '[Service]' >> $daemonspowerervice
echo 'Type=oneshot' >> $daemonspowerervice
echo 'ExecStart=/bin/sh -c ". /etc/profile; exec /usr/bin/python /storage/user/bin/deskpi-poweroff.py"' >> $daemonspowerervice
echo 'RemainAfterExit=yes' >> $daemonspowerervice
echo 'TimeoutSec=1' >> $daemonspowerervice
echo '[Install]' >> $daemonspowerervice
echo 'WantedBy=halt.target shutdown.target poweroff.target' >> $daemonspowerervice

chmod 644 $daemonspowerervice

echo "Successfully Built Power Service"

################################################################
################### Finish Up Install Script ###################
################################################################

echo "DeskPi Services and Daemons have been built."
echo "Installation of Deskpi Services and Daemons have Successfully finished"

############################
#######Stop Services########
############################

echo "DeskPi Service Load Modules."

systemctl daemon-reload
systemctl enable $daemonname-default.service
systemctl start $daemonname-default.service
systemctl daemon-reload
systemctl enable $daemonname-poweroff.service
systemctl start $daemonname-poweroff.service

echo -e "\e[31;40mSystemctl error\e[0m is because device\e[33;40m /dev/ttyUSB0\e[0m"
echo "has not been created yet, your device needs to reboot."

echo "Deskpi Services Loaded Correctly "

############################
#########Exit Code##########
############################

echo "Attempt to Remove Install Zip"
if [ -f "/storage/deskpi_isntaller.sh" ] ; then
rm -f /storage/deskpi_isntaller.sh
fi

echo "If Install Files were found, they were deleted."
echo "---------------------------------------------------------------"
echo "---------------------------------------------------------------"
echo "DeskPi Fan Control and PowerOff Service installed Successfully."
echo "System requires a reboot for settings to take effect."
echo "---------------------------------------------------------------"
echo "---------------------------------------------------------------"
