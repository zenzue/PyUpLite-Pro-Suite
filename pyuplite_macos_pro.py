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

def check_system_info():
    sys_info = execute_command("uname -a")
    results['System Info'] = sys_info

def check_sudo_permissions():
    sudo_check = execute_command("sudo -l")
    results['Sudo Permissions'] = sudo_check

def find_suid_sgid_files():
    suid_files = execute_command("find / -type f \\( -perm -4000 -o -perm -2000 \\) -exec ls -lh {} + 2>/dev/null")
    results['SUID_SGID Files'] = suid_files

def find_world_writable():
    writable_files = execute_command("find / -xdev -type f -perm -0002 -exec ls -lh {} + 2>/dev/null")
    writable_dirs = execute_command("find / -xdev -type d -perm -0002 -exec ls -ld {} + 2>/dev/null")
    results['World Writable Files'] = writable_files
    results['World Writable Directories'] = writable_dirs

def list_launch_agents_daemons():
    agents = execute_command("ls -alh /Library/LaunchAgents/ ~/Library/LaunchAgents/ /Library/LaunchDaemons/ 2>/dev/null")
    results['Launch Agents/Daemons'] = agents

def list_crontab_jobs():
    crontab_sys = execute_command("cat /etc/crontab 2>/dev/null")
    crontab_user = execute_command("crontab -l 2>/dev/null")
    results['System Crontab'] = crontab_sys
    results['User Crontab'] = crontab_user

def detect_docker_socket():
    if Path("/var/run/docker.sock").exists():
        info = execute_command("ls -l /var/run/docker.sock")
        results['Docker Socket'] = info
    else:
        results['Docker Socket'] = "No docker.sock found."

def check_sudoers_file():
    sudoers = execute_command("cat /etc/sudoers 2>/dev/null")
    results['Sudoers File'] = sudoers

def find_sensitive_files():
    sensitive = execute_command("find / -type f \\( -name '*.bak' -o -name '*.old' -o -name '*.swp' \\) 2>/dev/null")
    results['Sensitive Backup Files'] = sensitive

def check_env_variables():
    env_vars = dict(os.environ)
    interesting = {k: v for k, v in env_vars.items() if k in ["LD_PRELOAD", "DYLD_INSERT_LIBRARIES", "PATH", "HOME", "SHELL", "USER"]}
    results['Interesting Environment Variables'] = interesting

def export_to_json():
    with open("pyuplite_macos_report.json", "w") as f:
        json.dump(results, f, indent=4)
    print("\n[+] Results exported to pyuplite_macos_report.json")

def main():
    print("[*] PyUpLite-macOS-Pro - Advanced Privilege Escalation Scanner (Lab Use Only)")
    print()

    check_system_info()
    check_sudo_permissions()
    find_suid_sgid_files()
    find_world_writable()
    list_launch_agents_daemons()
    list_crontab_jobs()
    detect_docker_socket()
    check_sudoers_file()
    find_sensitive_files()
    check_env_variables()
    export_to_json()

    print("\n[+] Scan Completed. View results inside pyuplite_macos_report.json")

if __name__ == "__main__":
    main()