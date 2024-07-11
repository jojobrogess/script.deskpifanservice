import os
import xml.etree.ElementTree as ETree


class XMLParser:
    def __init__(self, parser_path):
        self.parser_path = parser_path
        self.tree = None
        self.root = None
        self.last_modified_time = 0
        self.load_xml()

    def load_xml(self):
        try:
            current_time = os.path.getmtime(self.parser_path)
            if current_time != self.last_modified_time:
                self.tree = ETree.parse(self.parser_path)
                self.root = self.tree.getroot()
                self.last_modified_time = current_time
        except OSError as e:
            print(f"Error accessing XML file: {e}")

    def get_mode(self):
        self.load_xml()
        return self._get_setting('mode')

    def _get_setting(self, setting_id):
        self.load_xml()
        return self.root.find(f'setting[@id="{setting_id}"]')

    def _check_setting(self, setting_id, default=None):
        self.load_xml()
        setting = self.root.find(f'setting[@id="{setting_id}"]')
        if setting is not None:
            return setting.text.lower() == 'true'
        return default

    def always_on(self):
        return self._check_setting('always_on', default=False)

    def turn_off(self):
        return self._check_setting('turn_off', default=False)

    def buffer_value(self):
        buffer_setting = self._get_setting('buffer')
        return buffer_setting

    def constant_value(self):
        speed_setting = self._get_setting('constant_value')
        speed = int(speed_setting.text.zfill(3))
        return [speed]

    def variable_values(self):
        temps = []
        speeds = []
        for i in range(1, 5):
            temp_setting = self._get_setting(f'temp{i}')
            speed_setting = self._get_setting(f'speed{i}')
            if temp_setting is not None and speed_setting is not None:
                temps.append(temp_setting.text)
                speeds.append(speed_setting.text.zfill(3))
        combined_values = [val for pair in zip(temps, speeds) for val in pair]
        return '\n'.join(map(str, combined_values))

    def overunder_values(self):
        fan_speed_under = int(self._get_setting('o_speed1').text.zfill(3))
        temp = int(self._get_setting('o_temp').text)
        fan_speed_over = int(self._get_setting('o_speed2').text.zfill(3))

        return fan_speed_under, temp, fan_speed_over


class SerialManager:
    def __init__(self, serial_param):
        self.serial_port = serial_param

    def send_serial(self, data):
        self.serial_port.write(data.encode())

    @staticmethod
    def mock_send_serial(data, cpu_temp=None):
        if data:
            if cpu_temp is not None:
                print(f"Current CPU temp: {cpu_temp} °C")
            print(f"Mock sending data: {data}")
        else:
            print("No data to send")

    @staticmethod
    def read_cpu_temp():
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as o:
                cpu_temp = int(o.read().strip()) // 1000
            return cpu_temp
        except FileNotFoundError:
            exit(1)
