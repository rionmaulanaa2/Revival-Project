# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Settle/EndCelebrateUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_0
import cc
from logic.gcommon import time_utility as tutil
from common.const import uiconst

class EndCelebrateUI(BasePanel):
    CELEBRATE_COUNTDOWN = 60
    PANEL_CONFIG_NAME = 'battle/fight_celebrate'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_0
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_leave.OnClick': 'on_click_leave_btn'
       }
    GLOBAL_EVENT = {'end_celebrate_win_state_event': 'end_celebrate_event'
       }

    def on_init_panel(self):
        self._close_cb = None
        self.panel.PlayAnimation('show')
        start_time = 2.0
        self.panel.SetTimeOut(start_time, lambda : self.panel.PlayAnimation('show_tips'))
        self.panel.SetTimeOut(start_time + self.panel.GetAnimationMaxRunTime('show_tips'), lambda : self.panel.PlayAnimation('loop_tips'))
        self.panel.SetTimeOut(start_time + self.panel.GetAnimationMaxRunTime('show_tips') + self.panel.GetAnimationMaxRunTime('loop_tips'), lambda : self.panel.PlayAnimation('hide_tips'))
        bat = global_data.player.get_battle()
        if bat:
            self.show_count_down(bat.get_settle_stage_arrive_time(), self.CELEBRATE_COUNTDOWN)
        return

    def set_close_callback(self, cb):
        self._close_cb = cb

    def on_click_leave_btn(self, btn, touch):
        if self.panel and self.panel.isValid():
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            dlg = SecondConfirmDlg2()

            def on_cancel():
                dlg.close()

            def on_confirm():
                dlg.close()
                self.close()
                if self._close_cb:
                    self._close_cb()
                    self._close_cb = None
                return

            dlg.confirm(content=get_text_local_content(19309), cancel_callback=on_cancel, confirm_callback=on_confirm, unique_callback=on_cancel)

    def show_count_down(self, start_time, count_down):
        ACT_TAG = 20201205
        start_time = start_time or tutil.get_server_time()
        end_t = start_time + count_down

        def func_count_down():
            cur_t = tutil.get_server_time()
            remain_count_down = int(end_t - cur_t)
            if remain_count_down <= 0:
                self.close()
                if self._close_cb:
                    self._close_cb()
                    self._close_cb = None
                return
            else:
                self.panel.lab_num.SetString(get_text_by_id(159).format(int(remain_count_down)))
                return

        self.panel.stopActionByTag(ACT_TAG)
        act = self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(func_count_down),
         cc.DelayTime.create(0.5)])))
        act.setTag(ACT_TAG)

    def end_celebrate_event(self):
        self.close()
        if self._close_cb:
            self._close_cb()
            self._close_cb = None
        return