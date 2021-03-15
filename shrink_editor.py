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

from anki.utils import pointVersion

from aqt import mw, gui_hooks
from aqt.editor import Editor


#config settings
def gc(arg="", fail=False):
    conf = mw.addonManager.getConfig(__name__)
    if conf:
        if arg:
            return conf.get(arg, fail)
        else:
            return conf
    return fail


def dc(arg="", fail=""):
    addon = mw.addonManager.addonFromModule(__name__)
    conf = mw.addonManager.addonConfigDefaults(addon)
    if conf:
        if arg:
            return conf.get(arg, fail)
        else:
            return conf
    return fail



addon_path = os.path.dirname(__file__)
addonfoldername = os.path.basename(addon_path)
source_absolute = os.path.join(addon_path, "sources", "css")
web_absolute = os.path.join(addon_path, "web", "css")

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
    with open(os.path.join(web_absolute, f), "w") as FO:
        FO.write(filecontent)


css_files_to_replace = [os.path.basename(f) for f in os.listdir(web_absolute) if f.endswith(".css")]
def replace_css(web_content, context):
    if isinstance(context, Editor):
        for filename in css_files_to_replace:
            web_content.css.append(f"/_addons/{addonfoldername}/web/css/{os.path.basename(filename)}")

gui_hooks.webview_will_set_content.append(replace_css)
