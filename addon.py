import os
import subprocess
import xbmcaddon
from pathlib import Path
from resources import utils as utils
file = '/storage/user/bin/deskpi.conf'
serial = '/dev/ttyUSB0'


class Main:

    # constructor of Main class
    def __init__(self):
        # Initialization of the Strings
        get_temp_1 = utils.get_setting('temp1')
        get_temp_2 = utils.get_setting('temp2')
        get_temp_3 = utils.get_setting('temp3')
        get_temp_4 = utils.get_setting('temp4')
        get_speed_1 = utils.get_setting('speed1')
        get_speed_2 = utils.get_setting('speed2')
        get_speed_3 = utils.get_setting('speed3')
        get_speed_4 = utils.get_setting('speed4')
        get_mode = utils.get_setting('get_mode')
        get_const_val = utils.get_setting('constant_val1')
        self.get_temp_1 = get_temp_1
        self.get_temp_2 = get_temp_2
        self.get_temp_3 = get_temp_3
        self.get_temp_4 = get_temp_4
        self.get_speed_1 = get_speed_1
        self.get_speed_2 = get_speed_2
        self.get_speed_3 = get_speed_3
        self.get_speed_4 = get_speed_4
        self.get_mode = get_mode
        self.get_const_val = get_const_val
        return

    def check_mode(self):
        if utils.get_setting('get_mode') == '0':
            self.write_constant()
        elif utils.get_setting('get_mode') == '1':
            self.write_custom()
        return

    def write_constant(self):
        self.stop_default_service()
        path = Path(file)
        if path.is_file():
            os.remove(file)
            get_const_val = "pwm_%s" % self.get_const_val.zfill(3)
            with open(serial, 'w') as c:
                c.writelines(get_const_val)
                c.close()
                utils.show_notification(utils.get_string(30024) + " " + self.get_const_val)
                utils.log(utils.get_string(30025) + " " + self.get_const_val)
            return

    def write_custom(self):
        self.stop_default_service()
        self.stop_constant()
        path = Path(file)
        if path.is_file():
            with open(file, 'r') as f:
                # read a list of lines into data
                lines = f.readlines()
            # now change the line, note that you have to add a newline
            get_temp_1 = self.get_temp_1
            get_temp_2 = self.get_temp_2
            get_temp_3 = self.get_temp_3
            get_temp_4 = self.get_temp_4            
            get_speed_1 = self.get_speed_1.zfill(3)
            get_speed_2 = self.get_speed_2.zfill(3)
            get_speed_3 = self.get_speed_3.zfill(3)
            get_speed_4 = self.get_speed_4.zfill(3)            
            lines[0] = '%s%s' % (get_temp_1, '\n')
            lines[2] = '%s%s' % (get_temp_2, '\n')
            lines[4] = '%s%s' % (get_temp_3, '\n')
            lines[6] = '%s%s' % (get_temp_4, '\n')
            lines[1] = '%s%s' % (get_speed_1, '\n')
            lines[3] = '%s%s' % (get_speed_2, '\n')
            lines[5] = '%s%s' % (get_speed_3, '\n')
            lines[7] = get_speed_4
            # create clean list for notification
            with open(file, 'r') as f:
                cleanlines = lines
                cleanlines = f.read().splitlines()
                f.close()
            # write everything back
            with open(file, 'w') as f:
                f.writelines(lines)
                f.close()
                utils.show_notification(utils.get_string(30025) + '\n' + str(cleanlines))
                utils.log(utils.get_string(30026) + '\n' + str(cleanlines))
                self.start_default_service()
        else:
            with open(file, 'w') as f:
                f.writelines(["30\n", "025\n", "35\n", "050\n", "40\n", "075\n", "45\n", "100"])
                f.close()
                self.start_default_service()
                self.write_custom()
            return

    def stop_constant(self):
        self.stop_default_service()
        with open(serial, 'w') as c:
            c.writelines("pwm_000")
            c.close()
        return

    def start_default_service(self):
        check = subprocess.run(["systemctl", "is-active", "deskpi-default"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if check.stdout != b"active\n":
            os.system("systemctl start deskpi-default.service")            
            return

    def stop_default_service(self):
        check = subprocess.run(["systemctl", "is-active", "deskpi-default"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if check.stdout == b"active\n":
            os.system("systemctl stop deskpi-default.service")
            return


if __name__ == '__main__':
    Main().check_mode()
