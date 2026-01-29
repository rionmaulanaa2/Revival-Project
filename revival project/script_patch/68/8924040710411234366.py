# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/prepare/AnchorVoiceTip.py
from __future__ import absolute_import
from common.const.uiconst import BASE_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_utils import parachute_utils
from common.utilities import get_utf8_length, cut_string_by_len
import common.utils.timer as timer
from common.const import uiconst

class AnchorVoiceTip(MechaDistortHelper, BasePanel):
    PANEL_CONFIG_NAME = 'battle_before/fight_before_host'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}

    def on_init_panel(self, *args, **kwargs):
        super(AnchorVoiceTip, self).on_init_panel(*args, **kwargs)
        self.switch_to_mecha()
        self.msg_text = None
        self.fade_in_timer = None
        self.text_index = 0
        self._switch = None
        self._priority = 0
        self._jump = False
        self._force_hide = False
        global_data.emgr.on_player_parachute_stage_changed += self.on_player_parachute_stage_changed
        return

    def on_player_parachute_stage_changed(self, stage):
        from logic.gcommon.common_utils.parachute_utils import STAGE_PARACHUTE_DROP
        if stage == STAGE_PARACHUTE_DROP:
            self.switch_to_non_mecha()

    def force_hide(self):
        self._force_hide = True

    def start_voice_tip(self, text, switch, priority):
        if self._force_hide:
            return
        if priority <= self._priority:
            return
        if self._switch:
            self.stop_voice_tip(self._switch)
        self._switch = switch
        self._priority = priority
        self.msg_text = text
        if global_data.player and global_data.player.logic and global_data.player.logic.ev_g_is_parachute_battle_land():
            from logic.gcommon.common_const.battle_const import UP_NODE_ANCHOR_VOICE
            global_data.emgr.battle_event_message.emit(text, message_type=UP_NODE_ANCHOR_VOICE)
            self.hide()
            self._jump = True
        else:
            self.show()
            self.panel.PlayAnimation('talking')
            self.text_fade_in()
            self._jump = False

    def text_fade_in(self):
        count = get_utf8_length(self.msg_text)
        self.text_index = 0

        def callback():
            self.text_index += 1
            if self.text_index >= count:
                self.text_index = count
            sub_text = cut_string_by_len(self.msg_text, self.text_index)
            self.panel.lab_describe.SetString(sub_text)

        if self.fade_in_timer:
            global_data.game_mgr.unregister_logic_timer(self.fade_in_timer)
        self.fade_in_timer = global_data.game_mgr.register_logic_timer(callback, interval=1, times=count, mode=timer.LOGIC)

    def stop_voice_tip(self, switch):
        if self._switch != switch:
            return
        else:
            self._switch = None
            self._priority = 0
            if self._jump:
                ui = global_data.ui_mgr.get_ui('BattleInfoVoice')
                if ui:
                    ui.on_finish()
            else:
                self.panel.StopAnimation('talking')
                self.hide()
                if self.fade_in_timer:
                    global_data.game_mgr.unregister_logic_timer(self.fade_in_timer)
                    self.fade_in_timer = None
            return

    def on_finalize_panel(self):
        if self.fade_in_timer:
            global_data.game_mgr.unregister_logic_timer(self.fade_in_timer)
            self.fade_in_timer = None
        global_data.emgr.on_player_parachute_stage_changed -= self.on_player_parachute_stage_changed
        return

    def get_text(self):
        if self._switch:
            return self.msg_text
        else:
            return None