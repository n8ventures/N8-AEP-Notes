import tkinter as tk
from tkinter import filedialog, ttk, PhotoImage, messagebox, scrolledtext
import os
import shutil
import sys
import atexit
import glob
import subprocess

# version info
from __version__ import __version__

# splash screen module
from modules.rootTkModule import (
    root
    )

from modules.TkModules import (
    make_non_resizable, center_window,
    Button
    )

# platform modules
from modules.platformModules import (
    win, mac,
    bundle_path,
    icon,
    license_file,
    icon_png
    )

# binary modules
from modules.BinaryModules import (
    jsxbin_file
    )

# info modules
from modules.infoModules import (
    watermark_label
    )

loading_screen = None

def detect_ae_paths():
    ae_versions = {}
    if win:
        base_paths = glob.glob(r"C:\Program Files\Adobe\Adobe After Effects *")
        for path in base_paths:
            panel_path = os.path.join(path, "Support Files", "Scripts", "ScriptUI Panels")
            if os.path.exists(panel_path):
                # Extract version name from path
                version_name = os.path.basename(path).replace("Adobe After Effects ", "")
                ae_versions[f"After Effects {version_name}"] = panel_path
    elif mac:
        base_paths = glob.glob("/Applications/Adobe After Effects *")
        for path in base_paths:
            panel_path = os.path.join(path, "Scripts", "ScriptUI Panels")
            if os.path.exists(panel_path):
                # Extract version name from path
                version_name = os.path.basename(path).replace("Adobe After Effects ", "")
                ae_versions[f"Adobe After Effects {version_name}"] = panel_path
    return ae_versions

def on_closing():
    print("Closing the application.")
    
    atexit.unregister(on_closing)  # Unregister the atexit callback
    root.destroy()

def license_window():
    global agree_var
    clear_screen()
    center_window(root, 600, 400)
    make_non_resizable(root)
    watermark_label(root)
    root.title(f"AEP Notes Installer v{__version__}")

    tk.Label(root, text="License Agreement (MIT)", font=("Arial", 14)).pack(pady=10)
    license_text = license_file
    txt = scrolledtext.ScrolledText(root, width=60, height=15, wrap=tk.WORD)
    txt.insert(tk.END, license_text)
    txt.configure(state="disabled")
    txt.pack(pady=10)

    agree_var = tk.BooleanVar()
    tk.Checkbutton(root, text="I agree to the terms and conditions", variable=agree_var).pack()
    Button(root, text="Next", command=check_agreement).pack(pady=20)

def check_agreement():
    if agree_var.get():
        show_detect_screen()
    else:
        messagebox.showwarning("Agreement Required", "Please agree to the terms before continuing.")

def show_detect_screen():
    center_window(root, 400, 250)
    clear_screen()
    tk.Label(root, text="Detected AE Installations", font=("Arial", 14)).pack(pady=10)

    detected_paths = detect_ae_paths()
    if not detected_paths:
        tk.Label(root, text="No installations detected.").pack(pady=5)

    path_var = tk.StringVar()
    if detected_paths:
        # Get list of program names for dropdown
        program_names = list(detected_paths.keys())
        dropdown = ttk.Combobox(root, textvariable=path_var, values=program_names, width=60, state="readonly")
        dropdown.pack(pady=10)
        dropdown.current(0)

    def install_selected():
        nonlocal path_var
        selected_path = path_var.get()
        if not selected_path:
            messagebox.showwarning("No Selection", "Please select an AE installation or use manual install.")
            return
        global target_dir
        target_dir = detected_paths[selected_path]
        install_jsxbin(target_dir)

    if detected_paths:
        Button(root, text="Install to Selected", command=install_selected).pack(pady=10)
    
    Button(root, text="Manual Install", command=manual_install).pack(pady=10)
    Button(root, text="Back", command=license_window).pack(pady=10)

def manual_install():
    center_window(root, 600, 300)
    global target_dir, install_status
    clear_screen()
    tk.Label(root, text="Select Install Location", font=("Arial", 14)).pack(pady=10)
    
    tk.Label(root, text="Locate your Adobe After Effects ScriptUI Panels folder.").pack(pady=5)
    Button(root, text="Browse", command=browse_folder).pack(pady=10)

    install_status = tk.Label(root, text="")
    install_status.pack(pady=10)

    target_dir = ""

def browse_folder():
    folder = filedialog.askdirectory(title="Select ScriptUI Panels folder")
    if folder:
        target_dir = folder
        install_status.config(text=f"Selected:\n{folder}")
        Button(root, text="Install", command=lambda: install_jsxbin(target_dir)).pack(pady=10)

def install_jsxbin(target_dir):
    if not os.path.isfile(jsxbin_file):
        messagebox.showerror("File Not Found", f"Cannot find {jsxbin_file}.")
        return

    if not target_dir:
        messagebox.showwarning("No Directory Selected", "Please select an install location first.")
        return

    try:
        destination = os.path.join(target_dir, os.path.basename(jsxbin_file))
        
        if mac:
            # Use osascript to trigger authentication dialog
            # Clean up paths for shell command
            def escape_path_for_applescript(path):
                path = path.replace("\\", "\\\\").replace('"', '\\"')
                path = os.path.normpath(path)
                return f'\\"{path}\\"'
            
            src_abs = os.path.abspath(jsxbin_file)
            dest_abs = os.path.abspath(target_dir)

            src_escaped = escape_path_for_applescript(src_abs)
            dest_escaped = escape_path_for_applescript(dest_abs)
            
            print(f"Copying {src_abs} to {dest_abs}")
            print("src_escaped: ", src_escaped)
            # Use ditto instead of cp for better macOS compatibility
            # NOTE: THIS DOES NOT WORK. 
            applescript_cmd = f'''
            do shell script "ditto {src_escaped} {dest_escaped}" with administrator privileges
            '''
            cmd = ['osascript', '-e', applescript_cmd]
            print("CMD: ", cmd)
            try:
                result = subprocess.run(
                    cmd,
                    check=True,
                    capture_output=True,
                    text=True
                )
                print(f"Command output: {result.stdout}")
            except subprocess.CalledProcessError as e:
                print(f"Error details: {e.stderr}")
                raise
        else:
            # Regular file copy for non-macOS systems
                shutil.copy2(jsxbin_file, destination)
        
        messagebox.showinfo("Success", "Installation Complete!")
        show_done()

    # except subprocess.CalledProcessError:
    #     messagebox.showerror("Error", "Installation cancelled or authentication failed.")
    except Exception as e:
        messagebox.showerror("Error", f"Installation failed: {e}")

def show_done():
    clear_screen()
    tk.Label(root, text="Installation Complete!", font=("Arial", 16)).pack(pady=20)
    Button(root, text="Open Install Directory", command=lambda: os.startfile(target_dir) if sys.platform=='win32' else os.system(f'open "{target_dir}"')).pack(pady=10)
    Button(root, text="Close", command=root.quit).pack(pady=10)

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

geo_width= 400
center_window(root, geo_width, 350)
make_non_resizable(root)
watermark_label(root)
root.title(f"AEP Notes Installer v{__version__}")
root.attributes('-topmost', True)

welcome_label = ttk.Label(root, text="Welcome to the AEP Notes Installer", font=("Helvetica", 16)).pack(pady=10)

start_button = Button(root, text="Start", command=license_window, width=20).pack(pady=20)

cancel_button = Button(root, text="Cancel", command=on_closing, width=20).pack(pady=20)

imgYPos = 225
image = PhotoImage(file=icon_png)
resized_image = image.subsample(8)
img_label = tk.Label(root, image=resized_image, bd=0)
img_label.place(x=geo_width / 2, y=imgYPos, anchor=tk.CENTER)
root.update_idletasks()

root.mainloop()