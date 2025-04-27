import os
import subprocess
import json
import win32api
import win32con
import win32security
import win32service
import win32serviceutil
import wmi
from pathlib import Path

results = {}

def execute_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
        return output.decode('utf-8', errors='ignore').strip()
    except subprocess.CalledProcessError:
        return ""
    except Exception as e:
        return str(e)

def check_system_info():
    system_info = execute_command("systeminfo")
    results['System Info'] = system_info

def check_uac_status():
    reg_path = 'HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System'
    output = execute_command(f'reg query "{reg_path}"')
    results['UAC Settings'] = output

def check_admin_rights():
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    results['Admin Privileges'] = "Yes" if is_admin else "No"

def find_unquoted_service_paths():
    c = wmi.WMI()
    unquoted_services = []
    for service in c.Win32_Service():
        if service.PathName and not service.PathName.startswith('"') and ' ' in service.PathName:
            unquoted_services.append(f"{service.Name}: {service.PathName}")
    results['Unquoted Service Paths'] = unquoted_services

def check_service_weak_permissions():
    c = wmi.WMI()
    weak_services = []
    for service in c.Win32_Service():
        try:
            if service.PathName:
                path = service.PathName.strip('"').split(' ')[0]
                if os.path.exists(path):
                    sd = win32security.GetFileSecurity(path, win32security.DACL_SECURITY_INFORMATION)
                    dacl = sd.GetSecurityDescriptorDacl()
                    for i in range(dacl.GetAceCount()):
                        ace = dacl.GetAce(i)
                        access_mask = ace[1]
                        user_sid = ace[2]
                        username, domain, _ = win32security.LookupAccountSid(None, user_sid)
                        if access_mask & (win32con.FILE_WRITE_DATA | win32con.FILE_APPEND_DATA):
                            weak_services.append(f"{service.Name}: {path} (Writable by {domain}\\{username})")
        except Exception:
            continue
    results['Weak Service Executable Permissions'] = weak_services

def list_auto_runs():
    autorun_paths = []
    keys = [
        r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run",
        r"HKLM\Software\Microsoft\Windows\CurrentVersion\Run"
    ]
    for key in keys:
        output = execute_command(f'reg query "{key}"')
        autorun_paths.append(output)
    results['Auto-Run Programs'] = autorun_paths

def check_token_privileges():
    token_privs = []
    try:
        hToken = win32security.OpenProcessToken(win32api.GetCurrentProcess(), win32con.TOKEN_QUERY)
        privileges = win32security.GetTokenInformation(hToken, win32security.TokenPrivileges)
        for priv_id, priv_flags in privileges:
            priv_name = win32security.LookupPrivilegeName(None, priv_id)
            if priv_flags & (win32con.SE_PRIVILEGE_ENABLED | win32con.SE_PRIVILEGE_ENABLED_BY_DEFAULT):
                token_privs.append(priv_name)
    except Exception as e:
        token_privs.append(str(e))
    results['Enabled Token Privileges'] = token_privs

def check_world_writable_path():
    path_env = os.environ.get('PATH', '')
    paths = path_env.split(';')
    writable_paths = []
    for p in paths:
        if os.path.isdir(p) and os.access(p, os.W_OK):
            writable_paths.append(p)
    results['World Writable PATH Directories'] = writable_paths

def find_sensitive_files():
    sensitive = execute_command('dir /s /b C:\\*.bak C:\\*.old C:\\*.swp 2>nul')
    results['Sensitive Backup Files'] = sensitive

def check_env_variables():
    env_vars = dict(os.environ)
    interesting = {k: v for k, v in env_vars.items() if k in ["USERNAME", "USERDOMAIN", "USERPROFILE", "HOMEPATH", "PATH", "TEMP"]}
    results['Interesting Environment Variables'] = interesting

def export_to_json():
    with open("pyuplite_windows_report.json", "w") as f:
        json.dump(results, f, indent=4)
    print("\n[+] Results exported to pyuplite_windows_report.json")

def main():
    print("[*] PyUpLite-Windows-Pro - Advanced Privilege Escalation Scanner (Lab Use Only)")
    print()

    check_system_info()
    check_uac_status()
    check_admin_rights()
    find_unquoted_service_paths()
    check_service_weak_permissions()
    list_auto_runs()
    check_token_privileges()
    check_world_writable_path()
    find_sensitive_files()
    check_env_variables()
    export_to_json()

    print("\n[+] Scan Completed. View results inside pyuplite_windows_report.json")

if __name__ == "__main__":
    main()

# pip install pywin32 wmi
