# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/art_check_ui/ArtCheckMainUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.const import uiconst
from logic.gcommon.common_const import scene_const

class ArtCheckMainUI(BasePanel):
    PANEL_CONFIG_NAME = 'art_check/art_check'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {}

    def on_init_panel(self, *args, **kargs):
        self.init_panel()
        self.init_parameters()

    def init_parameters(self):
        self.in_scenes = False

    def init_panel(self):
        self.panel.temp_button.btn_major.BindMethod('OnClick', self.on_click_btn_display)
        self.panel.temp_open_editor.btn_major.BindMethod('OnClick', self.on_click_btn_open_editor)

    def on_click_btn_display(self, *args):
        global_data.ui_mgr.show_ui('ArtCheckHumanDisplayUI', 'logic.comsys.art_check_ui')

    def on_click_btn_open_editor(self, *args):
        if global_data.artcheck_human_display_editor:
            return
        from editors import main_window
        main_window.start_human_editor()
        self.panel.temp_open_editor.setVisible(False)