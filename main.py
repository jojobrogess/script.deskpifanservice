import sys
from resources.install import Installer
from resources.uninstall import Uninstaller
from resources.install_integrity import Integrity
from resources.uninstall_integrity import UninstallIntegrity
from resources.restart_services import ServiceRestart
from resources.lib.utils import open_settings

installer = Installer()
uninstaller = Uninstaller()
integrity = Integrity()
uninstall_integrity = UninstallIntegrity()
restart_services = ServiceRestart()


def args():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == 'install':
            installer.install()
        elif arg == 'install_integrity':
            integrity.check_install()
        elif arg == 'uninstall':
            uninstaller.uninstall()
        elif arg == 'uninstall_integrity':
            uninstall_integrity.check_uninstall()
        elif arg == 'service_restart':
            restart_services.restart()
    else:
        open_settings()


if __name__ == "__main__":
    args()
