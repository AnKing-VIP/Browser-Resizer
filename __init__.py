from anki.hooks import wrap
from aqt.browser import Browser
from aqt import mw

# Use Config to customize

def setupSidebar_wrapper(self, *_):
    '''Reduce margins between items in Browser Sidebar'''
    config = mw.addonManager.getConfig(__name__)
    sidebar_margin = config.get("sidebar_margin", None)
    if not sidebar_margin:
        return
    style = f"QTreeView::item {{margin: -{sidebar_margin}px;}}"
    self.sidebarTree.setStyleSheet(style)

Browser.setupSidebar = wrap(Browser.setupSidebar, setupSidebar_wrapper)

def updateFont_wrapper(self, *_):
    '''Reduce row height in Browser table view'''
    config = mw.addonManager.getConfig(__name__)
    reduce_row_height_by = config.get("reduce_row_height_by", None)
    if not reduce_row_height_by:
        return
    vh = self.form.tableView.verticalHeader()
    original_height = vh.defaultSectionSize()
    new_height = original_height - reduce_row_height_by
    vh.setMinimumSectionSize(new_height)
    vh.setDefaultSectionSize(new_height)

Browser.updateFont = wrap(Browser.updateFont, updateFont_wrapper, 'after')
