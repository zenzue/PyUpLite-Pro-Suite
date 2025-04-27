import os
import subprocess
import json
from pathlib import Path

results = {}

def execute_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
        return output.decode().strip()
    except subprocess.CalledProcessError:
        return ""
    except Exception as e:
        return str(e)

def check_kernel_version():
    kernel = execute_command("uname -a")
    results['Kernel Version'] = kernel

def check_sudo_permissions():
    sudo_check = execute_command("sudo -l")
    results['Sudo Permissions'] = sudo_check

def find_suid_sgid_files():
    suid_files = execute_command("find / -type f \\( -perm -4000 -o -perm -2000 \\) -exec ls -lh {} + 2>/dev/null")
    results['SUID_SGID Files'] = suid_files

def find_world_writable_files():
    writable_files = execute_command("find / -xdev -type f -perm -0002 -exec ls -lh {} + 2>/dev/null")
    writable_dirs = execute_command("find / -xdev -type d -perm -0002 -exec ls -ld {} + 2>/dev/null")
    results['World Writable Files'] = writable_files
    results['World Writable Directories'] = writable_dirs

def list_crontab_jobs():
    crontabs = execute_command("cat /etc/crontab")
    user_crontab = execute_command("crontab -l")
    results['System Crontab'] = crontabs
    results['User Crontab'] = user_crontab

def list_running_services():
    services = execute_command("systemctl list-units --type=service --state=running")
    results['Running Services'] = services

def detect_docker_socket():
    if Path("/var/run/docker.sock").exists():
        info = execute_command("ls -l /var/run/docker.sock")
        results['Docker Socket Found'] = info
    else:
        results['Docker Socket Found'] = "No docker.sock found."

def readable_shadow():
    try:
        if os.access("/etc/shadow", os.R_OK):
            results['Readable /etc/shadow'] = "WARNING: /etc/shadow is readable!"
        else:
            results['Readable /etc/shadow'] = "Not readable (good)."
    except Exception as e:
        results['Readable /etc/shadow'] = str(e)

def check_uid0_users():
    passwd = Path("/etc/passwd").read_text(errors='ignore')
    uid0_users = [line.split(":")[0] for line in passwd.splitlines() if ":0:0:" in line]
    results['UID 0 Users'] = uid0_users

def find_sensitive_backup_files():
    sensitive_files = execute_command("find / -type f \\( -name '*.bak' -o -name '*.old' -o -name '*.swp' \\) 2>/dev/null")
    results['Backup/Swap Files Found'] = sensitive_files

def check_env_variables():
    env_vars = dict(os.environ)
    interesting = {k: v for k, v in env_vars.items() if k in ["LD_PRELOAD", "LD_LIBRARY_PATH", "PATH", "PWD", "USER", "HOME"]}
    results['Interesting Environment Variables'] = interesting

def check_nfs_exports():
    if Path("/etc/exports").exists():
        exports = Path("/etc/exports").read_text(errors='ignore')
        results['NFS Exports'] = exports
    else:
        results['NFS Exports'] = "No /etc/exports found."

def export_to_json():
    with open("pyuplite_linux_report.json", "w") as f:
        json.dump(results, f, indent=4)
    print("\n[+] Results exported to pyuplite_linux_report.json")

def main():
    print("[*] PyUpLite-Linux-Pro - Advanced Privilege Escalation Scanner (Lab Use Only)")
    print()

    check_kernel_version()
    check_sudo_permissions()
    find_suid_sgid_files()
    find_world_writable_files()
    list_crontab_jobs()
    list_running_services()
    detect_docker_socket()
    readable_shadow()
    check_uid0_users()
    find_sensitive_backup_files()
    check_env_variables()
    check_nfs_exports()
    export_to_json()

    print("\n[+] Scan Completed. View results inside pyuplite_linux_report.json")

if __name__ == "__main__":
    main()