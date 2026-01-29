# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartZombieFFAChooseMecha.py
from __future__ import absolute_import
from . import ScenePart

class PartZombieFFAChooseMecha(ScenePart.ScenePart):
    INIT_EVENT = {'enter_zombieffa_choose_mecha': 'init_choose_mecha_ui',
       'zombieffa_choose_mecha_finish': 'choose_mecha_finish'
       }

    def __init__(self, scene, name):
        super(PartZombieFFAChooseMecha, self).__init__(scene, name, need_update=False)
        self.ui = None
        return

    def init_choose_mecha_ui(self):
        if not global_data.video_player.is_in_init_state():
            global_data.video_player.stop_video(ignore_cb=True)
        self.ui = global_data.ui_mgr.show_ui('ZombieFFAChooseMechaUI', 'logic.comsys.battle.ZombieFFA')
        self.ui.enter_choose_mecha()

    def choose_mecha_finish(self):
        battle = global_data.battle
        if battle.choose_mecha_finish:
            battle.enter_battle()