import subprocess
import json
import os

results = {}

def adb_command(command):
    try:
        output = subprocess.check_output(f"adb shell {command}", shell=True, stderr=subprocess.DEVNULL)
        return output.decode().strip()
    except subprocess.CalledProcessError:
        return ""
    except Exception as e:
        return str(e)

def check_device_connection():
    devices = subprocess.getoutput("adb devices")
    if "device" not in devices.splitlines()[1]:
        print("[!] No Android device connected via ADB.")
        exit(1)

def get_device_info():
    results['Device Model'] = adb_command("getprop ro.product.model")
    results['Android Version'] = adb_command("getprop ro.build.version.release")
    results['Device Name'] = adb_command("getprop net.hostname")

def detect_root():
    su_check = adb_command("which su")
    root_status = "Rooted" if su_check else "Not Rooted"
    results['Root Access'] = root_status

def find_suid_sgid_files():
    suid_files = adb_command("find / -type f \\( -perm -4000 -o -perm -2000 \\) 2>/dev/null")
    results['SUID_SGID Files'] = suid_files

def find_world_writable_files():
    writable_files = adb_command("find / -xdev -type f -perm -0002 -exec ls -lh {} + 2>/dev/null")
    writable_dirs = adb_command("find / -xdev -type d -perm -0002 -exec ls -ld {} + 2>/dev/null")
    results['World Writable Files'] = writable_files
    results['World Writable Directories'] = writable_dirs

def list_running_processes():
    processes = adb_command("ps -A")
    results['Running Processes'] = processes

def list_installed_packages():
    packages = adb_command("pm list packages -f")
    results['Installed Packages'] = packages

def find_sensitive_files():
    sensitive = adb_command("find / -type f \\( -name '*.bak' -o -name '*.old' -o -name '*.swp' \\) 2>/dev/null")
    results['Sensitive Files'] = sensitive

def detect_dangerous_configs():
    adb_status = adb_command("getprop sys.usb.config")
    selinux_status = adb_command("getenforce")
    results['ADB USB Status'] = adb_status
    results['SELinux Mode'] = selinux_status

def export_to_json():
    with open("pyuplite_android_remote_report.json", "w") as f:
        json.dump(results, f, indent=4)
    print("\n[+] Results exported to pyuplite_android_remote_report.json")

def main():
    print("[*] PyUpLite-Android-Remote - Scan Android Device via ADB from Linux")
    print()

    check_device_connection()
    get_device_info()
    detect_root()
    find_suid_sgid_files()
    find_world_writable_files()
    list_running_processes()
    list_installed_packages()
    find_sensitive_files()
    detect_dangerous_configs()
    export_to_json()

    print("\n[+] Scan Completed. View results inside pyuplite_android_remote_report.json")

if __name__ == "__main__":
    main()