# Copyright: ijgnd
#            Ankitects Pty Ltd and contributors
# Modified by: The AnKing 
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html 


### Website: https://www.ankingmed.com  (Includes 40+ recommended add-ons)
### Youtube: https://www.youtube.com/theanking
### Instagram/Facebook: @ankingmed
### Patreon: https://www.patreon.com/ankingmed (Get individualized help)



# This is a simple solution without the new style hooks for basic changes of the style in the editor:
# from aqt import editor
# editor_style = """
# <style>
# </style>"""
# editor._html = editor_style + editor._html


import os
from pathlib import Path


from aqt import mw
from aqt import gui_hooks
from anki import version as anki_version

from .config import dc, gc


anki_point_version = int(anki_version.split(".")[2])


css_folder_for_anki_version = {
    "22": "22",
    "23": "22",
}


if anki_point_version in css_folder_for_anki_version:
    version_folder = css_folder_for_anki_version[v]
else:  # for newer Anki versions try the latest version and hope for the best
    version_folder = css_folder_for_anki_version[max(css_folder_for_anki_version, key=int)]


addon_path = os.path.dirname(__file__)
addonfoldername = os.path.basename(addon_path)
source_absolute = os.path.join(addon_path, "sources", "css", version_folder)
web_absolute = os.path.join(addon_path, "web", "css", version_folder)

regex = r"(web.*)"
mw.addonManager.setWebExports(__name__, regex)


# on startup: combine template files with config and write into webexports folder
for f in [os.path.basename(f) for f in os.listdir(source_absolute) if f.endswith(".css")]:
    with open(os.path.join(source_absolute, f)) as FO:
        filecontent = FO.read()
    for val in gc(): 
        if val in filecontent:
            newval = gc(val)
            if not newval:
                newval = dc(val)
            filecontent = filecontent.replace(val, str(newval))
    Path(web_absolute).mkdir(parents=True, exist_ok=True)
    with open(os.path.join(web_absolute, f), "w") as FO:
        FO.write(filecontent)


css_files_to_replace = [os.path.basename(f) for f in os.listdir(web_absolute) if f.endswith(".css")]
def replace_css(web_content, context):
    for idx, filename in enumerate(web_content.css):
        if filename in css_files_to_replace:
            web_content.css[idx] = f"/_addons/{addonfoldername}/web/css/{version_folder}/{filename}"



if anki_point_version >= 22 and gc("editor_shrink"):                    
    gui_hooks.webview_will_set_content.append(replace_css)
