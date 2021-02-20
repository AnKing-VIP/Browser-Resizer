# Copyright: ijgnd
#            Ankitects Pty Ltd and contributors
# Modified by: The AnKing 
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html 


### Website: https://www.ankingmed.com  (Includes 40+ recommended add-ons)
### Youtube: https://www.youtube.com/theanking
### Instagram/Facebook: @ankingmed
### Patreon: https://www.patreon.com/ankingmed (Get individualized help)


from .config import anki_point_version, gc


from . import browser_resizer


if gc("editor_shrink"):
    if anki_point_version < 22:
        print("editor shrinking not supported for older versions")
    elif 22 <= anki_point_version < 41:               
        from . import shrink_editor
    else:
        from . import shrink_editor_41up
