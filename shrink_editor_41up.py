# note about changes for 2.1.41
# For versions before 2.1.40 all relevant css changes were in the file editor.css
# In 2.1.41 the editor.css is loaded from two files: editor.css and editable.css
# see commits 7dc4b8818cb95a0c7043a3b2cd357551bc09bc88 and 61346cf1f70ececf7dafe0e8aa7f73571524b989 
# editable.css is loaded from editor.js. I can't overwrite this editable.css and
# patching editor.js looks complicated. So here I use a completely different approach and
# adjust the css after the editor was loaded with js using jquery.
# This approach should also work for older anki versions but I don't want to change
# what's been working for over half a year.


import os
from pathlib import Path

from aqt import mw
from aqt.gui_hooks import (
    editor_did_init,
)

addon_path = os.path.dirname(__file__)
addonfoldername = os.path.basename(addon_path)
source_absolute = os.path.join(addon_path, "sources", "css", "41")

regex = r"(sources[/\\]css[/\\]41.*)"
mw.addonManager.setWebExports(__name__, regex)


jsstring = f"""
$('head').append('<link rel="stylesheet" type="text/css" href="/_addons/{addonfoldername}/sources/css/41/diffonly__editable.css">');
$('head').append('<link rel="stylesheet" type="text/css" href="/_addons/{addonfoldername}/sources/css/41/diffonly__editor.css">');
"""

def adjust_css_with_js_after_editor_init(self):
    self.web.eval(jsstring)
editor_did_init.append(adjust_css_with_js_after_editor_init)
