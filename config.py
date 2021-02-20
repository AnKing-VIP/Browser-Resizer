from anki import version as anki_version
from aqt import mw


anki_point_version = int(anki_version.split(".")[2])


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
