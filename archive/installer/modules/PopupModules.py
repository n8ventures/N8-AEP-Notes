import tkinter as tk
from tkinter import ttk
import emoji

from __version__ import __version__
from modules.platformModules import icon, win, mac
from modules.TkModules import center_window

def create_popup(root, title, width, height, switch, lift = 0):
    popup = tk.Toplevel(root)
    center_window(popup, width, height)
    popup.title(title)

    if win:
        popup.iconbitmap(icon)

    # popup.overrideredirect(True)
    if win:
        popup.attributes('-toolwindow', 1)
    elif mac:
        popup.attributes('-type', 'utility')

    if switch == 1:
        popup.bind("<FocusOut>", lambda e: popup.after(200, popup.destroy))
    if lift == 1:
        popup.lift()

    popup.grab_set()
    return popup




