# Copyright: ijgnd
#            Ankitects Pty Ltd and contributors
# Modified by: The AnKing
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


### Website: https://www.ankingmed.com  (Includes 40+ recommended add-ons)
### Youtube: https://www.youtube.com/theanking
### Instagram/Facebook: @ankingmed
### Patreon: https://www.patreon.com/ankingmed (Get individualized help)


import os

from anki.utils import pointVersion

from aqt import mw
from aqt.gui_hooks import (
    webview_will_set_content,
    editor_did_load_note,
)
from aqt.editor import Editor


# config settings
def get_config(arg="", fail=False):
    conf = mw.addonManager.getConfig(__name__)
    if conf:
        if arg:
            return conf.get(arg, fail)
        else:
            return conf
    return fail


def default_config(arg="", fail=""):
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
for f in [
    os.path.basename(f) for f in os.listdir(source_absolute) if f.endswith(".css")
]:
    with open(os.path.join(source_absolute, f)) as FO:
        filecontent = FO.read()
    for val in get_config():
        if val in filecontent:
            newval = get_config(val)
            if not newval:
                newval = default_config(val)
            filecontent = filecontent.replace(val, str(newval))
    with open(os.path.join(web_absolute, f), "w") as FO:
        FO.write(filecontent)


def replace_css(web_content, context):
    if isinstance(context, Editor):
        web_content.css.append(
            f"/_addons/{addonfoldername}/web/css/editor.css"
        )


webview_will_set_content.append(replace_css)


def replace_css_editable(editor):
    editor.web.eval(f"""
var styleSheet = document.createElement("link");
styleSheet.rel = "stylesheet";
styleSheet.href = "_addons/{addonfoldername}/web/css/editable.css";

forEditorField([], (field) => {{
    if (!field.hasAttribute("has-browser-resizer")) {{
        field.editingArea.shadowRoot.appendChild(styleSheet.cloneNode(true))
        field.setAttribute("has-browser-resizer", "")
    }}
}})
""")


editor_did_load_note.append(replace_css_editable)
