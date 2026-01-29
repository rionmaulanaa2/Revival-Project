# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/CreditDownUI.py
from __future__ import absolute_import
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from logic.gutils.scene_utils import is_in_lobby

class CreditDownUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'role/honor_lv_down'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_close'
       }
    GLOBAL_EVENT = {'lobby_scene_pause_event': '_lobby_scene_event'
       }

    def on_init_panel(self):
        self.panel.PlayAnimation('appear')
        cur_scene = global_data.game_mgr.scene
        if not is_in_lobby(cur_scene.scene_type):
            self.add_hide_count()

    def _lobby_scene_event(self, pause_flag):
        if not pause_flag:
            self.clear_show_count_dict()

    def on_close(self, btn, touch):
        self.close()

    def show_level(self, level):
        self.panel.nd_level_up.lab_level.SetString(str(level))