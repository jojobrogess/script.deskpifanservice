import sys
import importlib
from resources.lib.utils import open_settings, show_dialog


def detect_os():
    try:
        with open('/etc/os-release', 'r') as file:
            os_info = file.read()
        if 'LibreELEC' in os_info:
            return 'libreelec'
        elif 'OSMC' in os_info:
            return 'osmc'
        else:
            return 'unknown'
    except FileNotFoundError:
        return 'unknown'


def args():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        os_name = detect_os()
        # show_dialog(f"Detected OS: {os_name}")  # Debugging line
        module_name = f"resources.os.{os_name}.{arg}"
        # show_dialog(f"Attempting to import module: {module_name}")  # Debugging line
        try:
            module = importlib.import_module(module_name)
            # Construct class name from arg
            class_name = ''.join([part.capitalize() for part in arg.split('_')])  # Convert to CamelCase
            # Get class from the module
            cls = getattr(module, class_name, None)
            if cls is not None:
                instance = cls()  # Create an instance of the class
                method = getattr(instance, arg, None)  # Get the method from the instance
                if method is not None and callable(method):
                    method()  # Call the method
                else:
                    show_dialog(
                        f"Method not found or not callable in class {class_name} of module {module_name}: {arg}")
            else:
                show_dialog(f"Class {class_name} not found in module {module_name}")
        except ImportError as e:
            show_dialog(f"ImportError: {str(e)}")  # Show the actual import error
            show_dialog(f"Unsupported OS: {os_name}")
    else:
        open_settings()


if __name__ == "__main__":
    args()
