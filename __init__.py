from .config import anki_point_version, gc


from . import browser_resizer


if gc("editor_shrink"):
    if anki_point_version < 22:
        print("editor shrinking not supported for older versions")
    elif 22 <= anki_point_version < 41:               
        from . import shrink_editor
    else:
        from . import shrink_editor_41up
