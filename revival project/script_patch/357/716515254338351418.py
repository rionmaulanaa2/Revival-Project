# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/NewAlphaPlan/AlphaPlanNewBieAttendUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const import uiconst
import render
from logic.comsys.activity.NewAlphaPlan.AlphaPlanNewbieAttendBase import AlphaPlanNewbieAttendBase

class AlphaPlanNewBieAttendUI(BasePanel, AlphaPlanNewbieAttendBase):
    PANEL_CONFIG_NAME = 'activity/activity_new_domestic/i_activity_8days'
    DLG_ZORDER = uiconst.NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'temp_btn_back.btn_back.OnClick': 'on_click_close_btn',
       'btn_sign_in.OnClick': 'on_click_get_reward'
       }
    GLOBAL_EVENT = {'update_newbie_attend_reward': '_on_update_newbie_attend_reward'
       }
    DELAY_REWARD_SHOW_TAG = 31415926

    def on_init_panel(self, *args, **kwargs):
        self._init_members()
        self._refresh_list_reward()
        self._refresh_progress()
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop_xlz')
        self.panel.PlayAnimation('loop_rg')
        self.panel.DelayCallWithTag(35 / self.FPS, self._play_reward_show, self.DELAY_REWARD_SHOW_TAG, len(self._reward_node_list) - 1, self.DELAY_REWARD_SHOW_TAG)
        global_data.display_agent.set_post_effect_active('gaussian_blur', True)
        self.hide_main_ui()

    def on_finalize_panel(self):
        global_data.display_agent.set_post_effect_active('gaussian_blur', False)
        self.show_main_ui()

    def do_hide_panel(self):
        BasePanel.do_hide_panel(self)
        global_data.display_agent.set_post_effect_active('gaussian_blur', False)

    def do_show_panel(self):
        BasePanel.do_show_panel(self)
        global_data.display_agent.set_post_effect_active('gaussian_blur', True)

    def _init_members(self):
        self._init_list_reward(self.panel.list_items, self.panel.temp_day8, self.panel.btn_sign_in, hide_ele=True)

    def on_click_close_btn(self, *args):
        self.close()