# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEBossDefeatUI.py
from __future__ import absolute_import
from logic.comsys.guide_ui.NewbieStageEndUI import NewbieStageEndUI
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.battle.BattleUtils import stop_self_fire_and_movement

class PVEBossDefeatUI(NewbieStageEndUI):
    MOUSE_CURSOR_TRIGGER_SHOW = False

    def on_init_panel(self, finish_cb=None):
        self.finish_cb = finish_cb
        global_data.sound_mgr.stop_music('pve')
        global_data.sound_mgr.play_music('firstplace')
        self.begin_show()
        self.panel.DelayCall(4.0, self.on_click_next)

    def on_finalize_panel(self):
        self.panel.stopAllActions()
        if self.show_next_timer:
            global_data.game_mgr.unregister_logic_timer(self.show_next_timer)
            self.show_next_timer = None
        return

    def begin_show(self):
        global_data.sound_mgr.play_ui_sound('bt_victory')
        self.panel.PlayAnimation('knockout_pve')
        self.panel.PlayAnimation('loop_pve')
        self.panel.nd_score.lab_score.SetString('')
        self.panel.nd_score.lab_score.icon_score.setVisible(False)
        self.show_next_timer = global_data.game_mgr.register_logic_timer(self.show_next, interval=28, times=1, args=('guide_new', ))

    def show_next(self, anim_name):
        super(PVEBossDefeatUI, self).show_next(anim_name)
        self.panel.nd_score.lab_score.setVisible(False)