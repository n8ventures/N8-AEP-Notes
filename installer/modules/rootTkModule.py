from tkinter import ttk, PhotoImage
import tkinter as tk
import sys
import sv_ttk
import darkdetect

from modules.TkModules import widget_color
from modules.platformModules import win, mac, icon

def set_args(argument = None):
    if argument is None:
        return False
    global args
    args = argument
    return True

root = tk.Tk()

print('TCL Library:', root.tk.exprstring('$tcl_library'))
print('Tk Library:',root.tk.exprstring('$tk_library'))

if win:
    root.iconbitmap(icon)
elif mac:
    root.iconphoto(True, PhotoImage(file=icon))

sv_ttk.set_theme(darkdetect.theme())
print('sv_ttk.get_theme(): ', sv_ttk.get_theme())

if win:
    import pywinstyles
    def apply_theme_to_titlebar():
        version = sys.getwindowsversion()
        print ('sys.getwindowsversion(): ', version)

        if version.major == 10 and version.build >= 22000:
            # Set the title bar color to the background color on Windows 11 for better appearance
            pywinstyles.change_header_color(root, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
        elif version.major == 10:
            pywinstyles.apply_style(root, "dark" if sv_ttk.get_theme() == "dark" else "normal")


            # A hacky way to update the title bar's color on Windows 10 (it doesn't update instantly like on Windows 11)
            root.wm_attributes("-alpha", 0.99)
            root.wm_attributes("-alpha", 1)

    apply_theme_to_titlebar()

style = ttk.Style()
style.configure("Alt.TLabel", foreground=widget_color[1])
style.configure("WM.TLabel", foreground='gray')
style.configure(
    "AltBox.TLabel",
    background="white", 
    relief="solid",      
    borderwidth=1,       
)
style.configure("Alt.TCheckbutton", foreground=widget_color[1])

# print(style.theme_names())  # List all themes
# print(style.layout("TLabel"))  # Display layout for 'TLabel'