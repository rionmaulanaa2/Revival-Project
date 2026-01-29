# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/PlayerTabBaseWidget.py


class PlayerTabBaseWidget(object):
    PANEL_CONFIG_NAME = 'undefined'

    def __init__(self, parent_panel):
        if self.PANEL_CONFIG_NAME == 'undefined':
            self.panel = parent_panel
        else:
            self.panel = global_data.uisystem.load_template_create(self.PANEL_CONFIG_NAME, parent_panel)

    def destroy(self):
        self.panel = None
        return

    def hide(self):
        if self.panel:
            self.panel.setVisible(False)

    def show(self):
        if self.panel:
            self.panel.setVisible(True)

    def on_appear(self):
        if self.panel:
            self.panel.PlayAnimation('in')

    def on_disappear(self):
        if self.panel:
            self.panel.PlayAnimation('out')

    def on_select(self, *args):
        pass

    def on_reset_states(self):
        pass

    def on_player_stat_inf(self, stat_inf):
        pass

    def on_refresh_player_detail_inf(self, player_inf):
        pass

    def jump_to_tab(self, tab, item_no=None):
        pass