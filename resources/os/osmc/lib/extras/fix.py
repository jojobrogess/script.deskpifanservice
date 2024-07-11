import subprocess


def add_start_x_to_config():
    config_path = '/boot/config-user.txt'
    new_line = 'start_x=1'

    try:
        # Remount the file system as read-write
        subprocess.run(["sudo", "mount", "-o", "remount,rw", "/boot"], check=True)

        # Use sudo to append the new line to the file
        subprocess.run(["sudo", "sh", "-c", f'echo "{new_line}" >> {config_path}'], check=True)

        print(f"Added '{new_line.strip()}' to {config_path}")

        # Remount the file system as read-only
        subprocess.run(["sudo", "mount", "-o", "remount,ro", "/boot"], check=True)

    except Exception as e:
        print(f"Error adding line to {config_path} with sudo: {str(e)}")


if __name__ == "__main__":
    add_start_x_to_config()
