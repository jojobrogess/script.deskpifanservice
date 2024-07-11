import os
import subprocess
from resources.lib.utils import addon_dir, get_string, show_dialog, log


class Install:
    def __init__(self):
        self.patterns = [
            'otg_mode=1',
            'dtoverlay=dwc2',
            'dr_mode=host',
            'dtoverlay=gpio-ir',
            'gpio_pin=17'
        ]
        self.services = [
            ("deskpi.service", 0o644),
            ("deskpi-poweroff.service", 0o644)
        ]
        self.old_install_paths = [
            "/storage/user/bin/deskpi-defaultcontrol.py",
            "/storage/.config/system.d/deskpi-default.service",
            "/storage/user/bin/deskpi-poweroff.py",
            "/storage/deskpi_installer.sh",
            "/storage/uninstall_deskpi.sh",
            "/storage/pyserial_installer.sh",
        ]

    def remove_old_installations(self):
        for path in self.old_install_paths:
            if os.path.exists(path):
                try:
                    os.remove(path)
                    log(__file__, f"Removed old installation file: {path}")
                except Exception as e:
                    log(__file__, f"Error removing old installation file {path}: {str(e)}")

    def install_flash(self):
        try:
            with open('/flash/config.txt', 'r') as flash_driver:
                flash_conf = flash_driver.read()
                missing_patterns = [
                    pattern + '\n' for pattern in self.patterns
                    if
                    all(pattern not in line.strip() or line.strip().startswith('#') for line in flash_conf.split('\n'))
                ]
                if missing_patterns:
                    missing_patterns_str = ", ".join(missing_patterns)
                    log(__file__, f"Config flag(s) {missing_patterns_str} missing.")
                    subprocess.run(["mount", "-o", "remount,rw", "/flash"])
                    with open('/flash/config.txt', 'a') as flash_writer:
                        flash_writer.writelines(missing_patterns)
                    subprocess.run(["mount", "-o", "remount,ro", "/flash"])
        except OSError as e:
            log(__file__, f"FATAL occurred while handling flash config: {str(e)}")

    def install_services(self):
        for service, permission in self.services:
            service_library = "/storage/.config/system.d/"
            service_driver_path = os.path.join(addon_dir(), "resources", "os", "libreelec", "lib", service)
            service_path = os.path.join(service_library, service)
            if not os.path.exists(service_path):
                try:
                    os.system(f'cp {service_driver_path} {service_library}')
                except Exception as copy_error:
                    log(__file__, f"Error copying {service}: {str(copy_error)}")
                try:
                    os.chmod(service_path, permission)
                except Exception as chmod_error:
                    log(__file__, f"Error changing permissions for {service}: {str(chmod_error)}")

    @staticmethod
    def start_services():
        servs = ["deskpi.service", "deskpi-poweroff.service"]
        try:
            subprocess.run(["systemctl", "daemon-reload"], check=True)
        except subprocess.CalledProcessError as daemon_error:
            log(__file__, f"Error reloading systemd: {str(daemon_error)}")
        for service in servs:
            try:
                subprocess.run(["systemctl", "enable", service], check=True)
                if service == "deskpi.service":
                    subprocess.run(["systemctl", "start", service], check=True)
            except subprocess.CalledProcessError as service_error:
                log(__file__, f"Error checking or starting '{service}': {service_error}")

    def install(self):
        self.remove_old_installations()
        self.install_flash()
        self.install_services()
        self.start_services()
        # line1 = "Deskpi Fan Service installed successfully!\n"
        # line2 = "Return to the settings page to customize your setup."
        show_dialog(get_string(30050))
        log(__file__, "Deskpi Fan Service installed successfully!")


if __name__ == "__main__":
    installer = Install()
    installer.install()
