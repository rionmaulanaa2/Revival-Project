# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleCommonRiko.py
from __future__ import absolute_import
from .BattleInfoMessage import BattleInfoMessage
from common.const.uiconst import BATTLE_MESSAGE_ZORDER, UI_TYPE_MESSAGE
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
from common.utilities import get_utf8_length, cut_string_by_len

class BattleCommonRiko(MechaDistortHelper, BattleInfoMessage):
    PANEL_CONFIG_NAME = 'battle_contention/battle_match_point_tips'
    DLG_ZORDER = BATTLE_MESSAGE_ZORDER
    UI_TYPE = UI_TYPE_MESSAGE
    UI_ACTION_EVENT = {}
    SHOW_TAG = 2112081638
    DURING_TAG = 2112081639
    DISAPPEAR_TAG = 2112081640

    def on_init_panel(self, on_process_done=None):
        super(BattleCommonRiko, self).on_init_panel(on_process_done)
        BattleInfoMessage.on_init_panel(self, on_process_done)
        self.msg_text = None
        self.text_index = 0
        self.finish_callback = None
        self._is_showing = False
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
        self.template_scale = message_data.get('template_scale', [0.5, 0.5])
        self.panel.nd_contention_riko_tips.setScale(self.template_scale[0], self.template_scale[1])
        self.show()
        self.panel.StopAnimation('disappear')
        self.panel.PlayAnimation('show')
        show_in_t = self.panel.GetAnimationMaxRunTime('show')
        self.panel.nd_contention_riko_tips.lab_tips.SetString('')
        self.panel.stopActionByTag(self.SHOW_TAG)
        self.panel.DelayCallWithTag(show_in_t, self.start_show, self.SHOW_TAG)

    def start_show(self):
        self.text_fade_in()
        self.panel.stopActionByTag(self.DURING_TAG)
        self.panel.DelayCallWithTag(self.delay_time, self.on_finish, self.DURING_TAG)

    def text_fade_in(self):
        count = get_utf8_length(self.msg_text)
        self.text_index = 0

        def add_one_char(dt):
            self.text_index += 1
            if self.text_index >= count:
                self.text_index = count
            sub_text = cut_string_by_len(self.msg_text, self.text_index)
            self.panel.nd_contention_riko_tips.lab_tips.SetString(sub_text)

        self.panel.TimerAction(add_one_char, 0.0333 * (count + 1), interval=0.0333)

    def on_finish(self):
        if not self._is_showing:
            return
        self._is_showing = False
        self.panel.stopActionByTag(1)
        self.panel.StopTimerAction()
        self.panel.StopAnimation('show')
        self.panel.PlayAnimation('disappear')
        show_out_t = self.panel.GetAnimationMaxRunTime('disappear')
        self.panel.stopActionByTag(self.DISAPPEAR_TAG)
        self.panel.DelayCallWithTag(show_out_t, self.tips_finish, self.DISAPPEAR_TAG)

    def tips_finish(self):
        if self.finish_callback:
            self.finish_callback()

    def on_finalize_panel(self):
        pass

    def on_click_bg_layer(self, btn, touch):
        self.on_finish()