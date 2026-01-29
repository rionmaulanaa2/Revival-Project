# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityNewbieAttendSub.py
from __future__ import absolute_import
from logic.client.const import mall_const
from logic.gutils import template_utils
from logic.gutils import item_utils
from logic.gutils import activity_utils
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name, get_lobby_item_desc
from logic.comsys.activity.NewAlphaPlan.AlphaPlanNewbieAttendBase import AlphaPlanNewbieAttendBase

class ActivityNewbieAttendSub(ActivityBase, AlphaPlanNewbieAttendBase):

    def __init__(self, dlg, activity_type):
        ActivityBase.__init__(self, dlg, activity_type)

    def on_init_panel(self):
        self._init_view()
        self._refresh_view()
        self.init_event()
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop_xlz')
        self.panel.PlayAnimation('loop_rg')
        self._play_reward_show(len(self._reward_node_list) - 1)

    def on_finalize_panel(self):
        self.process_event(False)

    def init_event(self):
        self.process_event(True)

    def _init_view(self):
        self._init_list_reward(self.panel.list_items, self.panel.temp_day8, self.panel.btn_sign_in, hide_ele=True)

        @self.panel.btn_sign_in.unique_callback()
        def OnClick(btn, touch):
            self.on_click_get_reward()

    def _refresh_view(self):
        self._refresh_list_reward()
        self._refresh_progress()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_newbie_attend_reward': self._on_update_newbie_attend_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_panel(self):
        self._refresh_view()

    def _on_update_newbie_attend_reward(self, *args):
        global_data.player.read_activity_list(self._activity_type)
        AlphaPlanNewbieAttendBase._on_update_newbie_attend_reward(self, *args)