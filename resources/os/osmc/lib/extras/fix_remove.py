import subprocess


def remount(mount_point):
    try:
        subprocess.run(["sudo", "mount", "-o", "remount,rw", mount_point], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error remounting {mount_point} as read-write: {e}")


def remove_line(path, line_to_remove):
    try:
        remount('/boot')
        with subprocess.Popen(["sudo", "cat", path], stdout=subprocess.PIPE) as proc:
            current_content = proc.stdout.read().decode()
        updated_content = '\n'.join(line for line in current_content.split('\n') if line.strip() != line_to_remove)
        sudo_cmd = ["sudo", "tee", path]
        with subprocess.Popen(sudo_cmd, stdin=subprocess.PIPE) as proc:
            proc.communicate(input=updated_content.encode())
    except Exception as e:
        print(f"Error removing line from {path} with sudo: {str(e)}")
    finally:
        subprocess.run(["sudo", "mount", "-o", "remount,rw", '/boot'], check=True)


file_path = '/boot/config-user.txt'
lines = 'start_x=1'
remove_line(file_path, lines)
