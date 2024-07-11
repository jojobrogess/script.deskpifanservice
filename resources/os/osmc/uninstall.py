import os
import subprocess
from resources.lib.utils import show_dialog, get_string, log


class Uninstall:
    def __init__(self):
        self.config_integrity = None
        self.service_integrity_uninstall = None
        self.service_integrity_start = None
        self.config = "/boot/config-user.txt"
        self.patterns = [
            'otg_mode=1',
            'dtoverlay=dwc2',
            'dr_mode=host',
            'dtoverlay=gpio-ir',
            'gpio_pin=17'
        ]
        self.service_library = "/lib/systemd/system/"
        self.services = [
            "deskpi.service",
            "deskpi-poweroff.service"
        ]

    def uninstall_config(self):
        config_messages = []
        try:
            subprocess.run(["sudo", "mount", "-o", "remount,rw", '/boot'], check=True)
            with subprocess.Popen(["sudo", "cat", self.config], stdout=subprocess.PIPE) as proc:
                current_content = proc.stdout.read().decode()
            patterns_missing = all(line.strip() != r for r in self.patterns for line in current_content.split('\n'))
            if patterns_missing:
                self.config_integrity = 'a'
            else:
                updated_content = '\n'.join(
                    line for line in current_content.split('\n') if all(line.strip() != r for r in self.patterns))
                sudo_cmd = ["sudo", "tee", self.config]
                with subprocess.Popen(sudo_cmd, stdin=subprocess.PIPE) as proc:
                    proc.communicate(input=updated_content.encode())
                    self.config_integrity = True
        except Exception as e:
            self.config_integrity = False
            config_messages.append(f"Error updating config file with sudo: {str(e)}")
        finally:
            subprocess.run(["sudo", "mount", "-o", "remount,rw", '/boot'], check=True)
        return config_messages, self.config_integrity

    def safe_remove(self, install_path, service_messages):
        try:
            subprocess.run(["sudo", "rm", install_path], check=True)
            self.service_integrity_uninstall = True
        except subprocess.CalledProcessError as e:
            if e.returncode != 1:  # Ignore error code 1 (FileNotFoundError)
                self.service_integrity_uninstall = False
                service_messages.append(f"Error removing {install_path} with sudo: {e}")
        return self.service_integrity_uninstall

    def uninstall_services(self):
        service_messages = []
        try:
            for service in self.services:
                services_path = os.path.join(self.service_library, service)
                if os.path.exists(services_path):
                    os.system("sudo systemctl daemon-reload")
                    os.system(f"sudo systemctl disable {service} 2&>/dev/null")
                    os.system("sudo systemctl daemon-reload")
                    os.system(f"sudo systemctl stop {service} 2&>/dev/null")
                    os.system("sudo systemctl daemon-reload")
                    services_paths = os.path.join(self.service_library, service)
                    self.safe_remove(services_paths, service_messages)
                    service_messages.append(f"{service}" + get_string(30053))
                else:
                    service_messages.append(f"{service} not found")
                    self.service_integrity_uninstall = 'a'
        except Exception as e:
            service_messages.append(f"{e}")
            self.service_integrity_uninstall = False
        return service_messages, self.service_integrity_uninstall

    def uninstall(self):
        config_messages, self.config_integrity = self.uninstall_config()
        service_messages, self.service_integrity_uninstall = self.uninstall_services()
        # show_dialog(str(self.config_integrity))
        # show_dialog(str(self.service_integrity_uninstall))
        combined_message = "\n".join(service_messages + config_messages)
        if self.config_integrity and self.service_integrity_uninstall == 'a':
            # line1 = "Deskpi Fan Service is already uninstalled.\n"
            # line2 = "Return to the settings page to customize your setup."
            show_dialog("Deskpi Fan Service is already uninstalled.")
        elif self.config_integrity and self.service_integrity_uninstall is True:
            # "All Deskpi files and services have been deleted.\n" \
            # "You can now uninstall the addon.\n" \
            # "Run integrity from troubleshooter to confirm.\n\n" + combined_message
            combined_messages = combined_message + "\n\n" + get_string(30054)
            show_dialog(combined_messages)
            log(__file__, "Deskpi Fan Service uninstalled successfully!")
        else:
            # line1 = "Deskpi Fan Service Uninstallation FAILED\n"
            # line2 = "Check and collect logs, please contact dev."
            show_dialog("Deskpi Fan Service Uninstallation FAILED" + "\n\n" + combined_message)


if __name__ == "__main__":
    uninstaller = Uninstall()
    uninstaller.uninstall()
