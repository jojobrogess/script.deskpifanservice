import subprocess
from resources.lib.utils import show_dialog, get_string


class RestartServices:
    def __init__(self):
        self.services = ["deskpi.service", "deskpi-poweroff.service"]

    def restart_services(self):
        messages = []
        all_services_running = True
        try:
            subprocess.run(["systemctl", "daemon-reload"], check=True)
        except subprocess.CalledProcessError as daemon_error:
            error_msg = get_string(30061) + f" {str(daemon_error)}"  # Error reloading systemd:
            messages.append(error_msg)
        for service in self.services:
            if service == "deskpi-poweroff.service":
                ignore_msg = get_string(30062) + f" '{service}'" + get_string(30063)  # Ignoring '{service}' as it is
                # not needed during active checks.
                messages.append(ignore_msg)
            else:  # Attempting to restart
                attempt_msg = get_string(30064) + f"'{service}'..."
                messages.append(attempt_msg)
                try:
                    subprocess.run(["systemctl", "restart", service], check=True)
                    success_msg = get_string(30065) + f" '{service}'" + get_string(
                        30066)  # Service '{service}' restarted successfully.
                    messages.append(success_msg)
                except subprocess.CalledProcessError as service_error:
                    error_msg = get_string(30067) + f" '{service}': {service_error}"
                    messages.append(error_msg)
                    all_services_running = False
        combined_message = "\n".join(messages)
        if all_services_running:
            show_dialog(combined_message)
        else:                  # Some services encountered issues during restart:
            error_dialog = get_string(30068) + "\n" + combined_message
            show_dialog(error_dialog)


if __name__ == "__main__":
    restarter = RestartServices()
    restarter.restart_services()
