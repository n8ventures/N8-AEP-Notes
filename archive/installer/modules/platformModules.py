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
license_file = None

icon_png = os.path.join(bundle_path or '', 'icon.png') if bundle_path else './icons/icon.png'

if win:
    icon = os.path.join(bundle_path or '', 'icon.ico') if bundle_path else './icons/icon.ico'
elif mac:
    icon = icon_png



if bundle_path:
    license_path = os.path.join(bundle_path, "LICENSE")
else:
    license_path = "../LICENSE"

    license_file = open(license_path).read() if os.path.exists(license_path) else "License file not found."

print("License file path:", license_path)
print("File exists:", os.path.exists(license_path))
print("Absolute path", os.path.abspath(license_path))