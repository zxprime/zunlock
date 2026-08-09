#!/usr/bin/env python3

import subprocess
import sys
import os
import urllib.request
import getpass

version = "1.5.9"

ORANGE = "\033[38;5;208m"
DIM = "\033[2m"
BOLD = "\033[1m"
RED = "\033[1;31m"
GREEN = "\033[1;32m"
RESET = "\033[0m"

PASSWORD_URL = "https://raw.githubusercontent.com/yourusername/yourrepo/main/password.txt"
MAX_ATTEMPTS = 3

TOOLS = {
    "1": ("Unlock Bootloader", "$PREFIX/bin/miunlock"),
    "2": ("Flash Fastboot ROM", "$PREFIX/bin/miflashf"),
    "3": ("Mi Assistant", "$PREFIX/bin/miasst"),
    "4": ("Firmware Content Extractor", "$PREFIX/bin/mifcetool")
}

try:
    term_width = os.get_terminal_size().columns
except:
    term_width = 80

def get_center(text):
    clean = text.replace(ORANGE, '').replace(RESET, '').replace(DIM, '')
    pad = (term_width - len(clean)) // 2
    return ' ' * pad + text

def check_password():
    try:
        with urllib.request.urlopen(PASSWORD_URL, timeout=10) as response:
            correct_password = response.read().decode('utf-8').strip()
    except Exception as e:
        print(f"{RED}✗ Error fetching password file: {e}{RESET}")
        sys.exit(1)

    for attempt in range(MAX_ATTEMPTS):
        try:
            entered = getpass.getpass(f"{BOLD}►{RESET} Enter password: ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{ORANGE}Cancelled{RESET}")
            sys.exit(0)

        if entered == correct_password:
            print(f"{GREEN}✓ Access granted{RESET}\n")
            return True
        else:
            remaining = MAX_ATTEMPTS - attempt - 1
            if remaining > 0:
                print(f"{RED}✗ Wrong password. {remaining} attempt(s) left{RESET}")
            else:
                print(f"{RED}✗ Access denied{RESET}")
                sys.exit(1)

check_password()

separator = f"{DIM}{'━' * min(term_width, 70)}{RESET}"

print("\n")
print(get_center(f"{DIM}{'═' * min(term_width, 70)}{RESET}"))

title = f"MiTool v{version}"
box_width = len(title) + 4
print(get_center(f"┏{'━' * (box_width - 2)}┓"))
print(get_center(f"┃  {ORANGE}MiTool{RESET} {DIM}v{version}{RESET}  ┃"))
print(get_center(f"┗{'━' * (box_width - 2)}┛"))

print(get_center(f"{DIM}github.com/offici5l/MiTool{RESET}"))
print(get_center(f"{DIM}{'═' * min(term_width, 70)}{RESET}"))
print()

print(f"{BOLD}Available Operations:{RESET}\n")
for key, (desc, _) in TOOLS.items():
    print(f"  {DIM}▸{RESET} [{ORANGE}{key}{RESET}] {desc}")
print(f"\n  {DIM}▸{RESET} [{ORANGE}q{RESET}] Quit\n")

if len(sys.argv) > 1:
    choice = sys.argv[1].lower()
    print(f"{ORANGE}►{RESET} Selected: {ORANGE}{choice}{RESET}\n")
else:
    try:
        choice = input(f"{BOLD}►{RESET} Enter choice: ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print(f"\n\n{ORANGE}Cancelled{RESET}")
        sys.exit(0)

if choice in ['q', 'quit', 'exit']:
    print(f"{ORANGE}Exiting...{RESET}\n")
    sys.exit(0)

if choice in TOOLS:
    desc, cmd = TOOLS[choice]
    print(f"\n{ORANGE}►{RESET} Executing: {DIM}{cmd}{RESET}\n")
    print(f"{DIM}{'─' * min(term_width, 70)}{RESET}\n")
    subprocess.run(cmd, shell=True)
else:
    print(f"{RED}✗ Invalid:{RESET} '{choice}'")
    print(f"{DIM}Select 1-4 or 'q' to quit{RESET}\n")
    sys.exit(1)