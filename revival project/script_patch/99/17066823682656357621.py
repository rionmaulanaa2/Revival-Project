# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleGooseBearRiko.py
from __future__ import absolute_import
from .BattleInfoMessage import BattleInfoMessage
from common.const.uiconst import BATTLE_MESSAGE_ZORDER, UI_TYPE_MESSAGE
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
from common.utils import timer
import time
import math

class BattleGooseBearRiko(MechaDistortHelper, BattleInfoMessage):
    PANEL_CONFIG_NAME = 'battle_happy_push/i_battle_happy_push_tips_warnning'
    DLG_ZORDER = BATTLE_MESSAGE_ZORDER
    UI_TYPE = UI_TYPE_MESSAGE
    UI_ACTION_EVENT = {}
    DURING_TAG = 2352915
    DISAPPEAR_TAG = 2352916

    def on_init_panel(self, on_process_done=None):
        super(BattleGooseBearRiko, self).on_init_panel(on_process_done)
        BattleInfoMessage.on_init_panel(self, on_process_done)
        self.msg_text = None
        self.text_index = 0
        self.finish_callback = None
        self._is_showing = False
        self.countdown_timer = None
        self.init_pos()
        return

    def init_pos(self):
        wpos = global_data.emgr.get_map_hint_wpos_event.emit()
        if wpos and len(wpos) > 0:
            lpos = self.panel.getParent().convertToNodeSpace(wpos[0])
            self.panel.setPosition(lpos)

    def process_one_message(self, message, finish_cb):
        self._is_showing = True
        self.finish_callback = finish_cb
        message_data = message[0]
        self.msg_text = message_data.get('content_txt', '')
        self.delay_time = message_data.get('delay_time', 5)
        self.template_scale = message_data.get('template_scale', [1.0, 1.0])
        self.panel.nd_ab.setScale(self.template_scale[0], self.template_scale[1])
        self.show()
        self.panel.StopAnimation('disappear')
        self.panel.PlayAnimation('appear')
        self.panel.lab_tips.SetString('')
        self.start_show()

    def start_show(self):
        self.show_countdown()
        self.panel.stopActionByTag(self.DURING_TAG)
        self.panel.DelayCallWithTag(self.delay_time, self.on_finish, self.DURING_TAG)

    def clear_timer(self):
        self.countdown_timer and global_data.game_mgr.get_logic_timer().unregister(self.countdown_timer)
        self.countdown_timer = None
        return

    def show_countdown(self):
        self.clear_timer()
        self.cur_time = time.time()

        def on_check():
            cur_time = time.time()
            left_time = max(int(math.ceil(self.delay_time - (cur_time - self.cur_time))), 0)
            self.panel.lab_tips.SetString(self.msg_text.format(str(left_time)))

        self.countdown_timer = global_data.game_mgr.get_logic_timer().register(func=on_check, mode=timer.CLOCK, interval=0.5)
        on_check()

    def on_finish(self):
        if not self._is_showing:
            return
        self._is_showing = False
        self.clear_timer()
        self.panel.StopTimerAction()
        self.panel.StopAnimation('appear')
        self.panel.PlayAnimation('disappear')
        show_out_t = self.panel.GetAnimationMaxRunTime('disappear')
        self.panel.stopActionByTag(self.DISAPPEAR_TAG)
        self.panel.DelayCallWithTag(show_out_t, self.tips_finish, self.DISAPPEAR_TAG)

    def tips_finish(self):
        if self.finish_callback:
            self.finish_callback()

    def on_finalize_panel(self):
        self.clear_timer()

    def on_click_bg_layer(self, btn, touch):
        self.on_finish()