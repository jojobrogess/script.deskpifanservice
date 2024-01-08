import subprocess
from utils import show_dialog, get_string

class ServiceRestart:
    def __init__(self):
        self.services = ["deskpi.service", "deskpi-poweroff.service"]

    def restart(self):
        messages = []
        all_services_running = True
        try:
            subprocess.run(["systemctl", "daemon-reload"], check=True)
        except subprocess.CalledProcessError as daemon_error:
            error_msg = get_string(30056) + f" {str(daemon_error)}" # Error reloading systemd:
            messages.append(error_msg)
        for service in self.services:
            if service == "deskpi-poweroff.service":
                ignore_msg = get_string(30057) + f" '{service}'" + get_string(30058)  # Ignoring '{service}' as it is not needed during active checks.
                messages.append(ignore_msg)
            else:            # Attempting to restart
                attempt_msg = get_string(30059) + f"'{service}'..."
                messages.append(attempt_msg)
                try:
                    subprocess.run(["systemctl", "restart", service], check=True)
                    success_msg = get_string(30060) + f" '{service}'" + get_string(30061) # Service '{service}' restarted successfully.
                    messages.append(success_msg)
                except subprocess.CalledProcessError as service_restart_error:
                    error_msg = get_string(30062) + f" '{service}': {service_restart_error}" # Error restarting
                    messages.append(error_msg)
                    all_services_running = False
        combined_message = "\n".join(messages)
        if all_services_running:
            show_dialog(combined_message)
        else:
            error_dialog = get_string(30063) + "\n" + combined_message # Some services encountered issues during restart:
            show_dialog(error_dialog)

if __name__ == "__main__":
    restarter = ServiceRestart()
    restarter.restart()
