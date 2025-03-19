import os
import sys
import platform
import subprocess
import tkinter as tk

# Check the platform
current_platform = platform.system()

win = current_platform == "Windows"
mac = current_platform == "Darwin"

def is_running_from_bundle():
    # Check if the application is running from a bundled executable
    if getattr(sys, 'frozen', False):
        if win:
            if hasattr(sys, '_MEIPASS'):
                return sys._MEIPASS
        if mac:
            current_dir = os.path.dirname(sys.executable)
            parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
            return os.path.join(parent_dir, "Resources")

    return False

from __version__ import __version__


if is_running_from_bundle():
    print("Running from a bundled application (.app/.exe)")
else:
    print("Running from source (.py)")

print("Current app version:", __version__)

print("Current working directory:", os.getcwd())
print("Executable path:", sys.executable)
print('TclVersion: ', tk.TclVersion)
print('TkVersion: ', tk.TkVersion)

# Handle bundle paths for binaries and icon
bundle_path = is_running_from_bundle()

icon = None

if any(char.isalpha() for char in __version__):
    if win:
        icon = os.path.join(bundle_path or '', 'icon.ico') if bundle_path else '.icons/icon.ico'
    elif mac:
        icon = os.path.join(bundle_path or '', 'icon.png') if bundle_path else './buildandsign/ico/ico3beta.png'
else:
    if win:
        icon = os.path.join(bundle_path or '', 'icon.ico') if bundle_path else 'icon/icon.ico'
    elif mac:
        icon = os.path.join(bundle_path or '', 'icon.png') if bundle_path else './icon/icon.png'
