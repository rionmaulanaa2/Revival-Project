# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityAnnivOpenReward.py
from __future__ import absolute_import
from .SimpleAdvance import SimpleAdvance
from logic.gutils.template_utils import init_tempate_mall_i_item

class ActivityAnnivOpenReward(SimpleAdvance):
    PANEL_CONFIG_NAME = 'activity/open_202201/open_reward'

    def on_init_panel(self, *args):
        super(ActivityAnnivOpenReward, self).on_init_panel()
        can_receive = not global_data.player.has_received_anniversary_reward(0)
        self.panel.btn_go.SetEnable(can_receive)
        self.panel.btn_go.SetText(get_text_by_id(604030 if can_receive else 604029))
        init_tempate_mall_i_item(self.panel.temp_item1, 71100004)

        @self.panel.btn_go.callback()
        def OnClick(*args):
            global_data.player.receive_anniversary_reward(0)
            self.panel.btn_go.SetEnable(False)
            self.panel.btn_go.SetText(get_text_by_id(604029))

    def get_close_node(self):
        return (
         self.panel.temp_btn_close.btn_back,)