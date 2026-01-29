# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleBuffUIPC.py
from __future__ import absolute_import
from .BattleBuffUI import BattleBuffBaseUI
from logic.comsys.effect import ui_effect
from logic.gcommon.common_const.buff_const import BUFF_SET_FIRE

class BattleBuffUIPC(BattleBuffBaseUI):
    PANEL_CONFIG_NAME = 'battle/battle_buff_ui_pc'

    def on_init_panel(self):
        self.mecha_state = False
        super(BattleBuffUIPC, self).on_init_panel()

    def on_finalize_panel(self):
        super(BattleBuffUIPC, self).on_finalize_panel()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_camera_target_setted_event': self.on_player_setted
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_player_setted(self):
        lplayer = global_data.cam_lplayer
        self.unbind_buff_event(lplayer)
        self.bind_buff_event(lplayer)

    def bind_buff_event(self, target):
        if not target:
            return
        target.regist_event('E_FIGHT_STATE_CHANGED', self.on_change_state)

    def unbind_buff_event(self, target):
        if not target:
            return
        target.unregist_event('E_FIGHT_STATE_CHANGED', self.on_change_state)

    def on_change_state(self, mecha_state=True):
        if not (self.panel and self.panel.isValid()):
            return