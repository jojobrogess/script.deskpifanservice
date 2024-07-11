import os
import subprocess
from resources.lib.utils import addon_dir, get_string, show_dialog, log


class Install:
    def __init__(self):
        self.config_integrity = None
        self.service_integrity_install = None
        self.service_integrity_start = None
        self.config = '/boot/config-user.txt'
        self.patterns = [
            'otg_mode=1',
            'dtoverlay=dwc2',
            'dr_mode=host',
            'dtoverlay=gpio-ir',
            'gpio_pin=17'
        ]
        self.service_library = ""
        self.services = [
            ("deskpi.service", 0o644),
            ("deskpi-poweroff.service", 0o644)
        ]

    def install_flash(self):
        try:
            with subprocess.Popen(["sudo", "cat", self.config], stdout=subprocess.PIPE) as proc:
                boot_conf = proc.stdout.read().decode()
                missing_patterns = [
                    pattern for pattern in self.patterns
                    if
                    all(pattern not in line.strip() or line.strip().startswith('#') for line in boot_conf.split('\n'))
                ]
                if missing_patterns:
                    missing_patterns_str = '\n'.join(missing_patterns)
                    subprocess.run(["sudo", "mount", "-o", "remount,rw", '/boot'], check=True)
                    subprocess.run(["sudo", "sh", "-c", f'echo "{missing_patterns_str}" >> {self.config}'], check=True)
                    subprocess.run(["sudo", "mount", "-o", "remount,ro", '/boot'], check=True)
                    self.config_integrity = True
                else:
                    self.config_integrity = 'a'
        except Exception as e:
            show_dialog(f"Error adding line to {self.config} with sudo: {str(e)}")
            self.config_integrity = False
        return self.config_integrity

    def install_services(self):
        for service, permission in [(s, p) for s, p in self.services if not os.path.exists(os.path.join(self.service_library, s))]:
            service_driver_path = os.path.join(addon_dir(), "resources", "os", "osmc", "lib", service)
            service_path = os.path.join(self.service_library, service)
            try:
                os.system(f'sudo cp {service_driver_path} {self.service_library}')
                subprocess.run(["sudo", "chmod", str(permission), service_path], check=True)
                self.service_integrity_install = True
            except Exception as install_error:
                self.service_integrity_install = False
                show_dialog(f"Error installing {service}: {str(install_error)}")
        else:
            self.service_integrity_install = 'a'
        return self.service_integrity_install

    @staticmethod
    def start_services():
        servs = ["deskpi.service", "deskpi-poweroff.service"]
        try:
            subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
        except subprocess.CalledProcessError as daemon_error:
            show_dialog(f"Error reloading systemd: {str(daemon_error)}")
        for service in servs:
            try:
                subprocess.run(["sudo", "systemctl", "enable", service], check=True)
                if service == "deskpi.service":
                    subprocess.run(["sudo", "systemctl", "start", service], check=True)
            except subprocess.CalledProcessError as service_error:
                show_dialog(f"Error checking or starting '{service}': {service_error}")

    def install(self):
        self.config_integrity = self.install_flash()
        self.service_integrity_install = self.install_services()
        # show_dialog(str(self.config_integrity))
        # show_dialog(str(self.service_integrity_install))
        self.start_services()
        if self.config_integrity and self.service_integrity_install == 'a':
            # line1 = "Deskpi Fan Service is already installed.\n"
            # line2 = "Return to the settings page to customize your setup."
            show_dialog("Deskpi Fan Service is already installed.")
        elif self.config_integrity and self.service_integrity_install is True:
            # line1 = "Deskpi Fan Service installed successfully!\n"
            # line2 = "Return to the settings page to customize your setup."
            show_dialog(get_string(30050))
            log(__file__, "Deskpi Fan Service installed successfully!")
        else:
            # line1 = "Deskpi Fan Service installed FAILED!\n"
            # line2 = "Check and collect logs, please contact dev."
            # show_dialog(get_string(30050))
            show_dialog("Deskpi Fan Service installation FAILED!")
            log(__file__, "Deskpi Fan Service installation FAILED!")


if __name__ == "__main__":
    installer = Install()
    installer.install()
