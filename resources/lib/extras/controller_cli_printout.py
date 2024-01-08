import os
import xml.etree.ElementTree as ETree
import time
import sys
import threading

serial_path = "/storage/.kodi/addons/script.deskpifanservice/resources/lib/"
sys.path.append(serial_path)
import serial


class XMLParser:
    def __init__(self, parser_path):
        self.parser_path = parser_path
        self.tree = None
        self.root = None
        self.last_modified_time = 0

    def load_xml(self):
        try:
            current_time = os.path.getmtime(self.parser_path)
            if current_time != self.last_modified_time:
                print(f"Current modification time: {current_time}")
                print("File modified. Reloading XML...")
                self.tree = ETree.parse(self.parser_path)
                self.root = self.tree.getroot()
                self.last_modified_time = current_time
                return True
        except OSError as e:
            print(f"Error accessing XML file: {e}")
        return False

    def get_settings(self):
        settings = {}
        if self.root is not None:
            for setting in self.root:
                settings[setting.attrib['id']] = setting.text
        return settings

    @staticmethod
    def read_cpu_temp():
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as o:
                cpu_temp = int(o.read().strip()) // 1000
            return cpu_temp
        except FileNotFoundError:
            exit(1)

    def print_associated_settings(self):
        cpu_temperature = self.read_cpu_temp()
        off = self.get_settings().get("turn_off", "-1")
        if off.lower() == "true":
            print("Turn Off Setting Found")
        elif off.lower() == "false":
            mode = self.get_settings().get("mode", "-1")
            if mode == "0":
                print(cpu_temperature)
                print("Current active mode: 0 (Constant)")
                print("Associated settings:")
                print("┌───────────┬────────┐")
                print("│ Setting   │ Value  │")
                print("├───────────┼────────┤")
                value = self.get_settings().get("constant_value", "")
                print(f"│ con_value │ {value:<6} │")
                print("└───────────┴────────┘")
            elif mode == "1":
                print(cpu_temperature)
                print("Current active mode: 1 (Variable)")
                variable_settings = [
                    "always_on", "temp1", "speed1", "temp2", "speed2",
                    "temp3", "speed3", "temp4", "speed4"
                ]
                print("Associated settings:")
                print("┌───────────┬────────┐")
                print("│ Setting   │ Value  │")
                print("├───────────┼────────┤")
                for setting in variable_settings:
                    value = self.get_settings().get(setting, '')
                    print(f"│ {setting:<9} │ {value:<6} │")
                print("└───────────┴────────┘")
            elif mode == "2":
                print(cpu_temperature)
                print("Current active mode: 2 (Overunder)")
                print("Associated settings:")
                print("┌───────────┬────────┐")
                print("│ Setting   │ Value  │")
                print("├───────────┼────────┤")
                buffer = self.get_settings().get("buffer", "")
                o_speed1 = self.get_settings().get("o_speed1", "")
                o_temp = self.get_settings().get("o_temp", "")
                o_speed2 = self.get_settings().get("o_speed2", "")
                print(f"│ Buffer    │ {buffer:<6} │")
                print(f"│ o_speed1  │ {o_speed1:<6} │")
                print(f"│ o_temp    │ {o_temp:<6} │")
                print(f"│ o_speed2  │ {o_speed2:<6} │")
                print("└───────────┴────────┘")


    def read_and_print_serial_data(self):
        port = '/dev/ttyUSB0'
        baudrate = 9600
        ser = serial.Serial(port, baudrate, timeout=1)
        while True:
            data = ser.read(1)
            if data:
                data += ser.read(ser.inWaiting())
                cleaned_data = data.decode("utf-8")
                # cleaned_data = data.decode().replace("b'", "").replace("'", "")
                print("┌───────────────┐")
                print(f"│ {cleaned_data:^13} │")
                print("└───────────────┘")

    def start_serial_monitor(self):
        serial_thread = threading.Thread(target=self.read_and_print_serial_data)
        serial_thread.start()


if __name__ == "__main__":
    xml_file_path = '/storage/.kodi/userdata/addon_data/script.deskpifanservice/settings.xml'
    xml_parser = XMLParser(xml_file_path)
    xml_parser.start_serial_monitor()

    while True:
        if xml_parser.load_xml():
            os.system('cls' if os.name == 'nt' else 'clear')
            xml_parser.print_associated_settings()
        time.sleep(5)
