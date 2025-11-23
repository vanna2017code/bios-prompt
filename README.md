# BIOS Simulator (Python)

A terminal-based simulation of a realistic BIOS/UEFI setup utility.  
This program mimics the look and feel of entering a BIOS environment, complete with POST splash, tabbed menus, configurable options, and persistent settings.

---

## ✨ Features

- **POST Splash Screen**
  - Displays vendor info, BIOS version, CPU, memory, and storage.
  - Simulates initialization messages (USB, SATA, NVRAM).
  - Prompts for entering Setup (`DEL` or `F2`).

- **Setup Utility Tabs**
  - **Main:** System date/time, language, fan control.
  - **Advanced:** Virtualization, hyper-threading, Intel RST, XMP profiles.
  - **Boot:** Boot mode, secure boot, boot order editor, fast boot.
  - **Security:** Admin password, TPM state, TPM clear.
  - **Exit:** Save/discard changes, exit options.

- **Interactive Editing**
  - Toggle boolean options (Enabled/Disabled).
  - Edit values with validation (date/time formats).
  - Reorder boot devices with index input.

- **Persistent Configuration**
  - Settings saved to `bios_config.json`.
  - Changes survive across runs.

- **Realistic Flow**
  - Save confirmation prompts.
  - Discard warnings if unsaved changes exist.
  - Simulated handoff to bootloader after exit.

---
## 🚀 Try it in GitHub Codespaces

Run this project instantly in a cloud-based dev environment:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/OWNER/REPO)

___
## 🖥️ Installation

1. Clone or download this repository.
2. Ensure you have **Python 3.7+** installed.
3. Run the program:

```bash
python bios_prompt.py
