#!/usr/bin/env python3
import os
import sys
import time
import json
from datetime import datetime

CONFIG_FILE = "bios_config.json"

DEFAULT_CONFIG = {
    "system": {
        "vendor": "American Megatrends Inc.",
        "bios_version": "P1.90",
        "build_date": "08/20/2024",
        "cpu": "Intel(R) Core(TM) i7-8700 CPU @ 3.20GHz",
        "memory": "16384 MB DDR4",
        "storage": ["Samsung SSD 970 EVO 500GB", "ST2000DM008-2FR102 2TB"]
    },
    "main": {
        "system_date": datetime.now().strftime("%m/%d/%Y"),
        "system_time": datetime.now().strftime("%H:%M:%S"),
        "language": "English",
        "fan_control": "Standard"
    },
    "advanced": {
        "virtualization": True,
        "hyper_threading": True,
        "intel_rst": False,
        "xmp_profile": "Auto"
    },
    "boot": {
        "boot_mode": "UEFI",
        "secure_boot": True,
        "boot_order": [
            "UEFI: Samsung SSD 970 EVO 500GB",
            "UEFI: USB Key",
            "UEFI: Network (IPv4)"
        ],
        "fast_boot": False
    },
    "security": {
        "admin_password_set": False,
        "tpm_state": "Enabled",
        "tpm_clear_pending": False
    }
}

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)

def pause(msg="Press Enter to continue..."):
    input(msg)

def draw_line(width=78):
    print("-" * width)

def post_splash(cfg):
    clear()
    vendor = cfg["system"]["vendor"]
    print(f"{vendor}")
    draw_line()
    print("AMIBIOS (C)2024 American Megatrends, Inc.")
    print(f"BIOS Version: {cfg['system']['bios_version']}   Build Date: {cfg['system']['build_date']}")
    print(f"CPU: {cfg['system']['cpu']}")
    print(f"Memory: {cfg['system']['memory']}")
    print(f"Storage: {', '.join(cfg['system']['storage'])}")
    draw_line()
    print("Initializing USB Controllers ... Done")
    time.sleep(0.5)
    print("Detecting SATA Devices ... Done")
    time.sleep(0.5)
    print("Checking NVRAM ... OK")
    time.sleep(0.5)
    draw_line()
    print("Press DEL or F2 to enter Setup")
    print("Press F11 for Boot Menu")
    time.sleep(1.5)

def header(title):
    print(f"UEFI/BIOS Setup Utility - {title}")
    draw_line()

def show_status_hints():
    print("[↑/↓] Select  [Enter] Edit/Toggle  [S] Save & Exit  [Q] Exit Without Saving")

def main_menu():
    print("Tabs:")
    print("  1) Main    2) Advanced    3) Boot    4) Security    5) Exit")

def edit_value(prompt, current, validator=None):
    print(f"{prompt} (current: {current})")
    new = input("> ").strip()
    if new == "":
        return current
    if validator:
        ok, msg = validator(new)
        if not ok:
            print(f"Invalid: {msg}")
            pause()
            return current
    return new

def toggle_bool(current):
    return not current

def list_editor(title, items):
    clear()
    header(title)
    print("Edit boot order: type indices to reorder, e.g., 2 1 3")
    for i, item in enumerate(items, 1):
        print(f"  {i}. {item}")
    choice = input("> ").strip()
    try:
        idxs = [int(x) for x in choice.split()]
        if sorted(idxs) != list(range(1, len(items)+1)):
            raise ValueError
        new_order = [items[i-1] for i in idxs]
        return new_order
    except Exception:
        print("No changes made.")
        pause()
        return items

def tab_main(cfg):
    while True:
        clear()
        header("Main")
        m = cfg["main"]
        print(f"1) System Date: {m['system_date']}")
        print(f"2) System Time: {m['system_time']}")
        print(f"3) Language:    {m['language']}")
        print(f"4) Fan Control: {m['fan_control']}   [Standard/Quiet/Performance]")
        draw_line()
        show_status_hints()
        print("Select item number or [B] Back")
        inp = input("> ").strip().lower()
        if inp == "b":
            return
        elif inp == "1":
            def v_date(s):
                try:
                    datetime.strptime(s, "%m/%d/%Y")
                    return True, ""
                except Exception:
                    return False, "Use MM/DD/YYYY"
            m["system_date"] = edit_value("Enter system date (MM/DD/YYYY)", m["system_date"], v_date)
        elif inp == "2":
            def v_time(s):
                try:
                    datetime.strptime(s, "%H:%M:%S")
                    return True, ""
                except Exception:
                    return False, "Use HH:MM:SS (24h)"
            m["system_time"] = edit_value("Enter system time (HH:MM:SS)", m["system_time"], v_time)
        elif inp == "3":
            m["language"] = edit_value("Language", m["language"])
        elif inp == "4":
            print("Choose Fan Profile: [Standard/Quiet/Performance]")
            m["fan_control"] = edit_value("Fan Control", m["fan_control"])
        elif inp == "s":
            return "save"
        elif inp == "q":
            return "quit"

def tab_advanced(cfg):
    while True:
        clear()
        header("Advanced")
        a = cfg["advanced"]
        print(f"1) Intel Virtualization Technology: {'Enabled' if a['virtualization'] else 'Disabled'}")
        print(f"2) Intel Hyper-Threading: {'Enabled' if a['hyper_threading'] else 'Disabled'}")
        print(f"3) Intel RST: {'Enabled' if a['intel_rst'] else 'Disabled'}")
        print(f"4) XMP Profile: {a['xmp_profile']}   [Auto/Profile1/Profile2]")
        draw_line()
        show_status_hints()
        print("Select item number or [B] Back")
        inp = input("> ").strip().lower()
        if inp == "b":
            return
        elif inp == "1":
            a["virtualization"] = toggle_bool(a["virtualization"])
        elif inp == "2":
            a["hyper_threading"] = toggle_bool(a["hyper_threading"])
        elif inp == "3":
            a["intel_rst"] = toggle_bool(a["intel_rst"])
        elif inp == "4":
            print("Choose XMP: [Auto/Profile1/Profile2]")
            a["xmp_profile"] = edit_value("XMP Profile", a["xmp_profile"])
        elif inp == "s":
            return "save"
        elif inp == "q":
            return "quit"

def tab_boot(cfg):
    while True:
        clear()
        header("Boot")
        b = cfg["boot"]
        print(f"1) Boot Mode: {b['boot_mode']}   [UEFI/Legacy]")
        print(f"2) Secure Boot: {'Enabled' if b['secure_boot'] else 'Disabled'}")
        print(f"3) Boot Order:")
        for i, item in enumerate(b["boot_order"], 1):
            print(f"   {i}. {item}")
        print(f"4) Fast Boot: {'Enabled' if b['fast_boot'] else 'Disabled'}")
        draw_line()
        show_status_hints()
        print("Select item number or [B] Back")
        inp = input("> ").strip().lower()
        if inp == "b":
            return
        elif inp == "1":
            b["boot_mode"] = "Legacy" if b["boot_mode"] == "UEFI" else "UEFI"
        elif inp == "2":
            b["secure_boot"] = toggle_bool(b["secure_boot"])
        elif inp == "3":
            b["boot_order"] = list_editor("Boot order", b["boot_order"])
        elif inp == "4":
            b["fast_boot"] = toggle_bool(b["fast_boot"])
        elif inp == "s":
            return "save"
        elif inp == "q":
            return "quit"

def tab_security(cfg):
    while True:
        clear()
        header("Security")
        s = cfg["security"]
        print(f"1) Administrator Password: {'Set' if s['admin_password_set'] else 'Not Set'}")
        print(f"2) TPM State: {s['tpm_state']}   [Enabled/Disabled]")
        print(f"3) TPM Clear Pending: {'Yes' if s['tpm_clear_pending'] else 'No'}")
        draw_line()
        show_status_hints()
        print("Select item number or [B] Back")
        inp = input("> ").strip().lower()
        if inp == "b":
            return
        elif inp == "1":
            if s["admin_password_set"]:
                confirm = input("Clear administrator password? [y/N]: ").strip().lower()
                if confirm == "y":
                    s["admin_password_set"] = False
            else:
                pw = input("Set new administrator password: ").strip()
                s["admin_password_set"] = bool(pw)
        elif inp == "2":
            s["tpm_state"] = "Disabled" if s["tpm_state"] == "Enabled" else "Enabled"
        elif inp == "3":
            s["tpm_clear_pending"] = toggle_bool(s["tpm_clear_pending"])
        elif inp == "s":
            return "save"
        elif inp == "q":
            return "quit"

def tab_exit(cfg):
    while True:
        clear()
        header("Exit")
        print("1) Save Changes and Exit")
        print("2) Discard Changes and Exit")
        print("3) Save Changes")
        print("4) Discard Changes")
        print("5) Return to Setup")
        draw_line()
        inp = input("> ").strip()
        if inp == "1":
            return "save_exit"
        elif inp == "2":
            return "discard_exit"
        elif inp == "3":
            return "save"
        elif inp == "4":
            return "discard"
        elif inp == "5":
            return "back"

def confirm_save():
    ans = input("Save configuration to NVRAM? [Y/n]: ").strip().lower()
    return ans in ("", "y", "yes")

def setup_loop(cfg):
    # Discard buffer for detecting changes
    baseline = json.dumps(cfg, sort_keys=True)
    while True:
        clear()
        header("Setup")
        main_menu()
        draw_line()
        show_status_hints()
        choice = input("> ").strip().lower()

        action = None
        if choice == "1":
            action = tab_main(cfg)
        elif choice == "2":
            action = tab_advanced(cfg)
        elif choice == "3":
            action = tab_boot(cfg)
        elif choice == "4":
            action = tab_security(cfg)
        elif choice == "5":
            exit_action = tab_exit(cfg)
            if exit_action == "save_exit":
                if confirm_save():
                    save_config(cfg)
                print("Exiting...")
                time.sleep(0.8)
                return
            elif exit_action == "discard_exit":
                print("Discarding changes...")
                time.sleep(0.8)
                return
            elif exit_action == "save":
                if confirm_save():
                    save_config(cfg)
                pause("Saved. Press Enter to return...")
            elif exit_action == "discard":
                pause("Discarded (not saved). Press Enter to return...")
            elif exit_action == "back":
                pass
        elif choice == "s":
            if confirm_save():
                save_config(cfg)
            pause("Saved. Press Enter to continue...")
        elif choice == "q":
            # Check if modified
            modified = baseline != json.dumps(cfg, sort_keys=True)
            if modified:
                ans = input("Discard unsaved changes and exit? [y/N]: ").strip().lower()
                if ans == "y":
                    print("Exiting...")
                    time.sleep(0.6)
                    return
            else:
                print("Exiting...")
                time.sleep(0.6)
                return

        if action == "save":
            if confirm_save():
                save_config(cfg)
            pause("Saved. Press Enter to continue...")
        elif action == "quit":
            modified = baseline != json.dumps(cfg, sort_keys=True)
            if modified:
                ans = input("Discard unsaved changes and exit? [y/N]: ").strip().lower()
                if ans == "y":
                    print("Exiting...")
                    time.sleep(0.6)
                    return
            else:
                print("Exiting...")
                time.sleep(0.6)
                return

def main():
    cfg = load_config()
    post_splash(cfg)
    setup_loop(cfg)
    clear()
    # Simulate handoff to bootloader
    print("Booting from:", cfg["boot"]["boot_order"][0])
    time.sleep(1.2)
    print("Loading operating system...")
    time.sleep(1.2)
    print("Done.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print("Interrupted.")
