# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/MechaDeath/MechaDeathRechooseMechaUI.py
from __future__ import absolute_import
from logic.comsys.battle.MechaSummonUI import MechaSummonUI
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon import time_utility

class MechaDeathRechooseMechaUI(MechaSummonUI):

    def on_init_panel(self, player):
        super(MechaDeathRechooseMechaUI, self).on_init_panel(player)
        self.init_count_down()

    def init_count_down(self):
        self.panel.nd_time.setVisible(False)
        battle = global_data.battle
        if not battle:
            return
        end_timestamp = battle.rechoose_mecha_end_timestamp
        left_time = end_timestamp - time_utility.get_server_time()

        def update_time(pass_time):
            new_left_time = int(left_time - pass_time)
            new_left_time_str = time_utility.get_delta_time_str(new_left_time)[3:]
            self.panel.nd_time.lab_time.SetString(new_left_time_str)
            self.panel.nd_time.lab_time_vx.SetString(new_left_time_str)
            if new_left_time <= 10:
                self.panel.PlayAnimation('alarm')

        self.panel.nd_time.lab_time.StopTimerAction()
        self.panel.nd_time.lab_time.TimerAction(update_time, left_time, callback=self.on_count_down_end, interval=1.0)
        self.panel.nd_time.setVisible(True)

    def on_count_down_end(self, *args):
        self.panel.nd_time.setVisible(False)

    def on_btn_call(self, *args):
        mecha_id = self.select_id
        if not mecha_id:
            return
        if not self.get_mecha_is_chooseable(mecha_id):
            global_data.emgr.battle_show_message_event.emit(get_text_by_id(18221))
            self.panel.btn_sure.SetShowEnable(False)
            return
        global_data.battle.do_rechoose_mecha(mecha_id)

    def on_click_close_btn(self, *args):
        if self.disappearing:
            return
        self.disappearing = True
        self.panel.PlayAnimation('quit')
        delay = self.panel.GetAnimationMaxRunTime('quit')
        self.panel.SetTimeOut(delay, lambda : self.close())
        global_data.battle.give_up_rechoose_mecha()
        global_data.ui_mgr.close_ui('MechaDeathPlayBackUI')