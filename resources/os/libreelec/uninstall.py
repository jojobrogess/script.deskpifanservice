import os
import subprocess
from resources.lib.utils import show_dialog, get_string, log


class Uninstall:
    def __init__(self):
        self.config = "/flash/config.txt"
        self.patterns = [
            'otg_mode=1',
            'dtoverlay=dwc2',
            'dr_mode=host',
            'dtoverlay=gpio-ir',
            'gpio_pin=17'
        ]
        self.service_library = "/storage/.config/system.d/"
        self.services = [
            "deskpi.service",
            "deskpi-poweroff.service"
        ]

    @staticmethod
    def safe_remove(install_path):
        try:
            os.remove(install_path)
        except FileNotFoundError:
            pass

    def uninstall_flash(self):
        messages = []
        try:
            with open(self.config, 'r') as flash_driver:
                flash_conf = flash_driver.readlines()
            removed_patterns = [
                line.strip() for line in flash_conf
                if any(pattern in line and not line.strip().startswith('#') for pattern in self.patterns)
            ]
            if removed_patterns:  # Config flags found and removed successfully.
                messages = get_string(30051)
                updated_conf = [line for line in flash_conf if line.strip() not in removed_patterns]
                subprocess.run(["mount", "-o", "remount,rw", "/flash"])
                with open(self.config, 'w') as flash_writer:
                    flash_writer.writelines(updated_conf)
                subprocess.run(["mount", "-o", "remount,ro", "/flash"])
            else:  # No matching config flags found or all have '#' in the line. Nothing to remove.
                messages = get_string(30052)
        except OSError as e:
            log(__file__, f"FATAL occurred while handling uninstalling flash config: {str(e)}")
        return messages

    def uninstall_services(self):
        messages = []
        for service in self.services:
            os.system("systemctl daemon-reload")
            os.system(f"systemctl disable {service} 2&>/dev/null")
            os.system("systemctl daemon-reload")
            os.system(f"systemctl stop {service} 2&>/dev/null")
            os.system("systemctl daemon-reload")
            file_path = os.path.join(self.service_library, service)
            self.safe_remove(file_path)  # service removed.
            messages.append(f"{service}" + get_string(30053))
        return messages

    def uninstall(self):
        messages_flash = self.uninstall_flash()
        messages_services = self.uninstall_services()
        combined_message = "\n".join(messages_services)
        # "All Deskpi files and services have been deleted.\n" \
        # "You can now uninstall the addon.\n" \
        # "Run integrity from troubleshooter to confirm.\n\n" + combined_message
        combined_messages = messages_flash + "\n" + combined_message + "\n\n" + get_string(30054)
        show_dialog(combined_messages)
        log(__file__, "Deskpi Fan Service uninstalled successfully!")


if __name__ == "__main__":
    uninstaller = Uninstall()
    uninstaller.uninstall()
