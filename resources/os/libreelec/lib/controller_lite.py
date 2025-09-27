import time
import sys
sys.path.append('/storage/.kodi/addons/virtual.rpi-tools/lib')
import RPi.GPIO as GPIO
from con_utils import XMLParser, PWMManager, read_cpu_temp


class Driver:
    def __init__(self, _file_path, rename):
        self.parser = XMLParser(_file_path)
        self.pwm_manager = PWMManager(rename)
        self.read_cpu_temp = read_cpu_temp
        self.min_temp = 0
        self.data = ""

    def _change_fan_speed(self, current_speed, new_speed, wait_time=10):
        if new_speed != current_speed:
            self.pwm_manager.send_pwm(new_speed)
            current_speed = new_speed
            if self.parser.turn_off():
                print("Turn_Off Setting Found, Turning Off Fan")
        else:
            time.sleep(wait_time)
        return current_speed

    def run(self):
        try:
            current_speed = None
            while True:
                if self.parser.turn_off():
                    self.pwm_manager.stop()
                    current_speed = self._change_fan_speed(current_speed, self.data)

                else:
                    mode_element = self.parser.get_mode()
                    mode = mode_element.text if mode_element is not None else "No mode found"
                    print(f"Mode: {mode}")
                    cpu_temp = self.read_cpu_temp()
                    print(f"Current CPU Temp: {cpu_temp}°C")

                    if mode == '0':
                        c_value = self.parser.constant_value()
                        self.data = f"{c_value[0]:03d}"

                    if mode == '1':
                        v_values = self.parser.variable_values()
                        pairs = [(int(v_values.split('\n')[i]), int(v_values.split('\n')[i + 1]))
                                 for i in range(0, len(v_values.split('\n')), 2)]
                        non_zero_pairs = [pair for pair in pairs if pair != (0, 0)]
                        if self.parser.always_on():
                            lowest_temp_pair = min(non_zero_pairs, key=lambda x: x[0])
                            if cpu_temp < lowest_temp_pair[0]:
                                self.data = f"{lowest_temp_pair[1]:03d}"
                            else:
                                for temp, speed in non_zero_pairs:
                                    if cpu_temp >= temp:
                                        self.data = f"{speed:03d}"
                        else:
                            lowest_temp = min([pair[0] for pair in pairs])
                            if cpu_temp < lowest_temp:
                                self.data = self.pwm_manager.stop()
                            else:
                                for temp, speed in pairs:
                                    if cpu_temp >= temp:
                                        self.data = f"{speed:03d}"

                    elif mode == '2':
                        fan_speed_under, temp, fan_speed_over = self.parser.overunder_values()
                        if temp >= cpu_temp:
                            speed = fan_speed_under
                        else:
                            speed = fan_speed_over
                        self.data = f"{speed:03d}"

                    current_speed = self._change_fan_speed(current_speed, self.data)

        except KeyboardInterrupt:
            self.pwm_manager.stop()


if __name__ == "__main__":
    file_path = '/storage/.kodi/userdata/addon_data/script.deskpifanservice/settings.xml'
    parser_instance = XMLParser(file_path)
    pwm_pin = int(parser_instance.get_pin())
    driver_instance = Driver(file_path, pwm_pin)

    try:
        driver_instance.run()
    except KeyboardInterrupt:
        driver_instance.pwm_manager.stop()
    finally:
        GPIO.cleanup()

