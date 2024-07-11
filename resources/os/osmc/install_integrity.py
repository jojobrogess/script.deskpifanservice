import os
from resources.lib.utils import get_string, show_dialog, log


class InstallIntegrity:
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
            ("deskpi.service", 0o644),
            ("deskpi-poweroff.service", 0o644)
        ]

    def check_config(self):
        messages = []
        try:
            with open(self.config, 'r') as flash_driver:
                flash_conf = flash_driver.readlines()
            missing_patterns = [
                pattern for pattern in self.patterns
                if all(pattern not in line.strip() or line.strip().startswith('#') for line in flash_conf)
            ]
            if missing_patterns:
                missing_patterns_str = "\n".join(missing_patterns)
                # Configuration file is the missing flags:
                messages = get_string(30055) + f"\n{missing_patterns_str}"
                self.config_integrity = False
            else:  # Configuration integrity check passed.
                messages = get_string(30056)
                self.config_integrity = True
        except OSError as e:
            log(__file__, f"FATAL occurred while handling uninstalling flash config: {str(e)}")
            self.config_integrity = False
        return messages, self.config_integrity

    def check_services(self):
        service_messages = []
        for services, _ in self.services:
            service_path = os.path.join(self.service_library, services)
            try:
                if not os.path.exists(service_path):
                    service_messages.append(services)
            except Exception as e:
                log(__file__, f"FATAL Error running installation integrity check for {services}: {str(e)}")
        if service_messages:  # Service files missing:
            missing_services_message = get_string(30057) + "\n" + "\n".join(service_messages)
            self.service_integrity = False
        else:  # Service integrity check passed.
            missing_services_message = get_string(30058)
            self.service_integrity = True
        return missing_services_message, self.service_integrity

    def install_integrity(self):
        config_messages, self.config_integrity = self.check_config()
        service_messages, self.service_integrity = self.check_services()
        combined_messages = f"{config_messages}\n{service_messages}"

        if self.config_integrity and self.service_integrity:
            # line1 = "Deskpi Fan Service Integrity Check: PASSED.\n"
            # line2 = "If you're still having issues, please contact dev."
            show_dialog(combined_messages + "\n\n" + get_string(30059))
        else:
            # line1 = "Deskpi Fan Service Integrity Check: FAILED.\n"
            # line2 = "Check and collect logs, please contact dev."
            show_dialog(get_string(30060) + "\n\n" + combined_messages)


if __name__ == "__main__":
    integrity = InstallIntegrity()
    integrity.install_integrity()
