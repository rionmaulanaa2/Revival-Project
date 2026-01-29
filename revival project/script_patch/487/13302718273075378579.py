# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/MobileInfoUI.py
from __future__ import absolute_import
from common.const.uiconst import BASE_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from common.const import uiconst

class MobileInfoUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/fight_setting'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_feedback.OnClick': 'on_click_feedback'
       }

    def on_click_feedback(self, *args):
        from logic.comsys.feedback import echoes
        from logic.comsys.feedback.echoes import BATTLE
        echoes.show_feedback_view(BATTLE)

    def on_init_panel(self):
        self.init_event()

    def init_event(self):
        self.cur_camera_state_type = None
        partCamera = global_data.game_mgr.scene.get_com('PartCamera')
        if partCamera:
            self.on_camera_switch_to_state(partCamera.get_cur_camera_state_type())
        emgr = global_data.emgr
        econf = {'camera_switch_to_state_event': self.on_camera_switch_to_state
           }
        emgr.bind_events(econf)
        return

    def on_camera_switch_to_state(self, state, *args):
        from logic.client.const import camera_const
        if state == camera_const.AIM_MODE:
            self.add_hide_count('AIM_CAMERA')
        elif self.cur_camera_state_type == camera_const.AIM_MODE and state != camera_const.AIM_MODE:
            self.add_show_count('AIM_CAMERA')
        self.cur_camera_state_type = state