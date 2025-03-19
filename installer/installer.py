import tkinter as tk
from tkinter import filedialog, ttk, colorchooser, PhotoImage
from PIL import Image, ImageTk
import subprocess
import os
import shutil
import sys
import atexit
from idlelib.tooltip import Hovertip
import threading
import time
import math
import re
import glob

# version info
from __version__ import __version__

# splash screen module
from installer.modules.rootTkModule import (
    root
    )

# tk popups and settings
from modules.PopupModules import (
    create_popup
    )

from modules.TkModules import (
    make_non_resizable, center_window,
    Button, widget_color,
    )

from modules.platformModules import (
    win, mac,
    bundle_path,
    icon
    )

# info modules
from modules.infoModules import watermark_label

loading_screen = None


def on_closing():
    print("Closing the application.")
    
    atexit.unregister(on_closing)  # Unregister the atexit callback
    root.destroy()

geo_width= 425
center_window(root, geo_width, 450)
make_non_resizable(root)
watermark_label(root)

root.mainloop()