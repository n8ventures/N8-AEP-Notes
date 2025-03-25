import os
from modules.platformModules import bundle_path

if bundle_path:
    jsxbin_file = "N8's AEP Notes.jsxbin"
else:
    jsxbin_file = "../N8's AEP Notes.jsxbin" if os.path.exists("../N8's AEP Notes.jsxbin") else "../src/N8's AEP Notes.jsx"