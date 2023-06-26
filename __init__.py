import os

from aqt import mw

# from . import browser_resizer
# from . import shrink_editor


def replace_module_name_in_config_help():
    """Replace static add-on module name in config.md with the actual name"""

    path = os.path.join(mw.addonManager.addonsFolder(
        mw.addonManager.addonFromModule(__name__)), "config.md")
    with open(path, encoding="utf-8") as f:
        contents = f.read()
        contents = contents.replace(
            "/_addons/1435775540", f"/_addons/{mw.addonManager.addonFromModule(__name__)}")
        return contents


# Make images available to the config help webview
mw.addonManager.setWebExports(__name__, r"AnKing/.*")
if hasattr(mw.addonManager, 'set_config_help_action'):
    mw.addonManager.set_config_help_action(mw.addonManager.addonFromModule(
        __name__), replace_module_name_in_config_help)
