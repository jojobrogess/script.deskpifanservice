import os
from resources.lib.utils import get_string, show_dialog, log


class UninstallIntegrity:
    def __init__(self):
        self.config_integrity = None
        self.service_integrity = None
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

    def check_config(self):
        config_messages = []
        try:
            with open(self.config, 'r') as flash_driver:
                flash_conf = flash_driver.readlines()
            patterns_found = [
                pattern for pattern in self.patterns
                if any(pattern in line.strip() and not line.strip().startswith('#') for line in flash_conf)
            ]
            if patterns_found:
                existing_patterns = "\n".join(patterns_found)
                # Flags found:
                messages_str = get_string(30069) + f"\n{existing_patterns}"
                # Config integrity check failed.
                config_messages = get_string(30070) + f"\n{messages_str}"
                self.config_integrity = False
            else:                   # Configuration integrity check passed.
                config_messages = get_string(30071)
                self.config_integrity = True
        except OSError as e:
            log(__file__, f"FATAL occurred while handling uninstalling flash config: {str(e)}")
            self.config_integrity = False
        return config_messages, self.config_integrity

    def check_services(self):
        service_messages = []
        for services in self.services:
            service_path = os.path.join(self.service_library, services)
            try:
                if os.path.exists(service_path):  # still exist.
                    services_str = f"{services}" + get_string(30072)
                    service_messages.append(services_str)
                    self.service_integrity = False
                else:
                    self.service_integrity = True
            except Exception as e:
                log(__file__, f"Error running installation integrity check for {services}: {str(e)}")
                self.service_integrity = False
        if self.service_integrity:     # Service integrity check passed.
            service_messages.append(get_string(30073))
        return ' '.join(service_messages), self.service_integrity

    def uninstall_integrity(self):
        config_messages, self.config_integrity = self.check_config()
        service_messages, self.service_integrity = self.check_services()
        combined_messages = f"{config_messages}\n{service_messages}"

        if self.config_integrity and self.service_integrity:
            # line1 = "Deskpi Fan Service Integrity Check Passed:\n"
            # line2 = "If you're still having issues, please contact dev."
            show_dialog(combined_messages + "\n\n" + get_string(30074))
        else:
            # line1 = "Deskpi Fan Service Integrity Check FAILED:\n"
            # line2 = "Check and collect logs, please contact dev."
            show_dialog(get_string(30075) + "\n\n" + combined_messages)


if __name__ == "__main__":
    integrity = UninstallIntegrity()
    integrity.uninstall_integrity()
