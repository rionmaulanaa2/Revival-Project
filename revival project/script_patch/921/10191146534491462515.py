# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/parachute_ui/ParachutePlaneUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_utils.parachute_utils import STAGE_FREE_DROP, STAGE_PLANE, STAGE_FLY_CARRIER
from common.const import uiconst

class ParachutePlaneUI(BasePanel):
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'parachute/plane_rocker'
    UI_ACTION_EVENT = {'btn_parachute.OnClick': 'on_click_parachute',
       'btn_parachute.OnBegin': 'on_begin_parachute',
       'btn_parachute.OnEnd': 'on_end_parachute'
       }

    def on_init_panel(self, *args, **kwargs):
        self.set_parachute_texture()
        self.init_event()

    def init_event(self):
        global_data.emgr.plane_stage_start_event += self.set_btn_visible

    def set_parachute_texture(self, *args):
        lavatar = global_data.player.logic
        if not lavatar:
            raise
        self.btn_parachute.setVisible(global_data.player.get_battle()._plane_start)

    def set_btn_visible(self):
        self.btn_parachute.setVisible(True)

    def on_click_parachute(self, *args):
        global_data.emgr.player_try_switch_parachute_stage.emit()
        self.close()
        return True

    def on_begin_parachute(self, *args):
        return True

    def on_end_parachute(self, *args):
        pass