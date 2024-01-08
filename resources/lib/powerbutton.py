import os
import sys

addon_dir = '/storage/.kodi/addons/script.deskpifanservice/'
serial_path = os.path.join(addon_dir, "resources", "lib")
sys.path.append(serial_path)

import serial


class SerialController:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600, timeout=30):
        self.serial_port = serial.Serial(port, baudrate=baudrate, timeout=timeout)

    def send_serial(self, data):
        if self.serial_port.isOpen():
            self.serial_port.write(data.encode())

    def power_off(self):
        self.send_serial('power_off')
        self.serial_port.close()

    def run(self):
        try:
            while True:
                self.power_off()

        except KeyboardInterrupt:
            self.power_off()


if __name__ == "__main__":
    controller = SerialController()
    controller.run()
