# PyUpLite-Pro Suite

## Overview

PyUpLite-Pro is a suite of lightweight, advanced privilege escalation enumeration tools for macOS, Linux, and Windows.  
It is designed for ethical red team operations, security research, and controlled lab environments.

Each version is specialized for its respective operating system, providing passive scanning of potential privilege escalation vectors without performing any exploitation.

---

## Versions

### PyUpLite-macOS-Pro

- System and Kernel information enumeration
- Sudo permissions listing
- SUID and SGID file discovery
- World-writable files and directories identification
- Launch Daemon and Launch Agent enumeration
- User and system crontab job listing
- Docker socket abuse detection
- `/etc/sudoers` file inspection
- Backup and swap file discovery
- Sensitive environment variable inspection
- Export results to structured JSON report

### PyUpLite-Linux-Pro

- Kernel version and system information enumeration
- Sudo permissions inspection
- SUID and SGID file discovery
- World-writable files and directories identification
- User and system crontab job enumeration
- Running services listing
- Docker socket abuse detection
- `/etc/shadow` readability check
- UID 0 user enumeration
- Backup and swap file discovery
- Environment variable inspection
- NFS exports configuration discovery
- Export results to structured JSON report

### PyUpLite-Windows-Pro

- Windows version and system information enumeration
- UAC settings inspection
- Admin privilege detection
- Unquoted service paths discovery
- Weak service executable permissions identification
- Auto-run programs listing from registry
- Token privilege enumeration (SeDebug, SeImpersonate, etc.)
- Writable directories in system PATH
- Sensitive backup file detection
- Environment variable inspection
- Export results to structured JSON report

---

## Installation

1. Ensure Python 3 is installed:
    ```bash
    python3 --version
    ```

2. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/pyuplite-pro.git
    cd pyuplite-pro
    ```

3. Install required Python packages:

For macOS/Linux:

```bash
pip install -r requirements.txt
```

For Windows:

```bash
pip install pywin32 wmi
```

---

## Usage

### macOS

```bash
python3 pyuplite_macos_pro.py
```

### Linux

```bash
python3 pyuplite_linux_pro.py
```

### Windows

```bash
python pyuplite_windows_pro.py
```

Upon completion, each script will generate a structured JSON report with the findings.

---

## Output

Each script generates a corresponding JSON report:

- `pyuplite_macos_report.json`
- `pyuplite_linux_report.json`
- `pyuplite_windows_report.json`

The reports contain organized findings under various categories for easier review, triage, and reporting.

---

## Ethical Notice

PyUpLite-Pro tools are strictly intended for educational purposes, authorized penetration testing, controlled red team exercises, and research environments.

Unauthorized use against systems without explicit permission is prohibited and may violate laws and regulations.

---

## Author

Aung Myat Thu (w01f)

---

## License

This project is licensed for educational and research purposes only.  
No warranties are provided. Use at your own risk.