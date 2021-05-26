# Modified by: The AnKing
### Website: https://www.ankingmed.com  (Includes 40+ recommended add-ons)
### Youtube: https://www.youtube.com/theanking
### Instagram/Facebook: @ankingmed
### Patreon: https://www.patreon.com/ankingmed (Get individualized help)

from anki.hooks import wrap
from aqt.browser import Browser
from aqt import mw
from anki.utils import pointVersion


# Use Config to customize
config = mw.addonManager.getConfig(__name__)


def setupSidebar_wrapper(self, *_):
    """Reduce margins between items in Browser Sidebar"""
    sidebar_margin = config.get("sidebar_margin", None)
    if not sidebar_margin:
        return
    style = f"QTreeView::item {{margin: -{sidebar_margin}px;}}"
    self.sidebarTree.setStyleSheet(style)


Browser.setupSidebar = wrap(Browser.setupSidebar, setupSidebar_wrapper)


def updateFont_wrapper(self, *_):
    """Reduce row height in Browser table view"""
    reduce_row_height_by = config.get("reduce_row_height_by", None)
    if not reduce_row_height_by:
        return
    vh = self.form.tableView.verticalHeader()
    original_height = vh.defaultSectionSize()
    new_height = original_height - reduce_row_height_by
    vh.setMinimumSectionSize(new_height)
    vh.setDefaultSectionSize(new_height)

if pointVersion() < 45: 
    Browser.updateFont = wrap(Browser.updateFont, updateFont_wrapper, "after")
