# Copyright: ijgnd
# Modified by: The AnKing 
### Website: https://www.ankingmed.com  (Includes 40+ recommended add-ons)
### Youtube: https://www.youtube.com/theanking
### Instagram/Facebook: @ankingmed
### Patreon: https://www.patreon.com/ankingmed (Get individualized help)
#
#            Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html 

import os

from anki.utils import pointVersion

from aqt import mw
from aqt import gui_hooks
from anki import version as anki_version

#config settings
def gc(arg, fail=False):
    conf = mw.addonManager.getConfig(__name__)
    if conf:
        return conf.get(arg, fail)
    return fail

css_folder_for_anki_version = {
    "21": "21",
    "22": "21",  # for Anki version 22 use the contents of the folder 21 
}
js_folder_for_anki_version = {
}


v = pointVersion()
if v in css_folder_for_anki_version:
    my_css_folder = css_folder_for_anki_version[v]
else:  # for newer Anki versions try the latest version and hope for the best
    my_css_folder = css_folder_for_anki_version[max(css_folder_for_anki_version, key=int)]

addon_path = os.path.dirname(__file__)
addonfoldername = os.path.basename(addon_path)
my_css_folder_absolute = os.path.join(addon_path, "web", "css", my_css_folder)

mycssfiles = [os.path.basename(f) for f in os.listdir(my_css_folder_absolute) if f.endswith(".css")]

regex = r"(web.*)"
mw.addonManager.setWebExports(__name__, regex)

#file_to_open = editor 
if gc("editor field font size") != "none":
    fontset = "font-size:" + gc("editor field font size") + "!important;"
else:    
    fontset = ""


#overwrite editor.css with user font size info
with open(f"/{addon_path}/editor.css") as f: 
    filecontent = f.read() 
    completed = filecontent.format(fontsize = fontset)
with open(f"/{addon_path}/web/css/{my_css_folder}/editor.css", "w") as o: 
    o.write(completed) 

def replace_css(web_content, context):
    for idx, filename in enumerate(web_content.css):
        if filename in mycssfiles:
            web_content.css[idx] = f"/_addons/{addonfoldername}/web/css/{my_css_folder}/{filename}"


old_anki = tuple(int(i) for i in anki_version.split(".")) < (2, 1, 22)

if not old_anki and gc("editor_shrink"):                    
    gui_hooks.webview_will_set_content.append(replace_css)
