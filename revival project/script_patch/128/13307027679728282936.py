# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ZombieFFA/ZombieFFAPlayBackUI.py
from __future__ import absolute_import
from logic.comsys.battle.Death.DeathPlayBackUI import DeathPlayBackUI
import cc

class ZombieFFAPlayBackUI(DeathPlayBackUI):
    MOUSE_CURSOR_TRIGGER_SHOW = True
    UI_ACTION_EVENT = {'nd_change.btn_change.OnClick': 'on_click_btn_mutate'
       }

    def on_init_panel(self):
        super(ZombieFFAPlayBackUI, self).on_init_panel()
        self.panel.nd_change.setVisible(False)
        self.panel.icon_change.setVisible(False)
        self.panel.icon_change_ffa3.setVisible(True)
        _, pos_y = self.panel.nd_change.GetPosition()
        self.panel.nd_change.SetPosition('50%', pos_y + 15)

    def init_panel(self):
        super(ZombieFFAPlayBackUI, self).init_panel()
        if global_data.player and global_data.player.logic:
            is_in_spec = global_data.player.logic.ev_g_is_in_spectate()
            if is_in_spec:
                self.panel.nd_change.setVisible(False)

    def on_click_btn_mutate(self, *args):
        player = global_data.player
        if not player:
            return
        battle = player.get_battle() or player.get_joining_battle()
        battle and battle.start_combat(mutation=True)

    def count_down_start(self):
        super(ZombieFFAPlayBackUI, self).count_down_start()
        self.panel.nd_change.setVisible(False)

    def count_down_over(self):
        super(ZombieFFAPlayBackUI, self).count_down_over()
        self.init_btn_change_visible()

    def init_btn_change_visible(self):
        player = global_data.player
        if not player or not player.logic:
            return
        is_in_spec = global_data.player.logic.ev_g_is_in_spectate()
        bat = player.get_battle() or player.get_joining_battle()
        is_visible = bat.enable_mutation and not bat.is_mutated and not is_in_spec
        self.panel.nd_change.setVisible(is_visible)
        if is_visible:
            self.play_btn_change_anim()

    def play_btn_change_anim(self):
        action = self.panel.runAction(cc.Sequence.create([
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show_panel')),
         cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('show_panel')),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop')),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop2'))]))