# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartFFAChooseMecha.py
from __future__ import absolute_import
from . import ScenePart
from common.utils import timer

class PartFFAChooseMecha(ScenePart.ScenePart):
    INIT_EVENT = {'enter_ffa_choose_mecha': 'init_choose_mecha_ui',
       'ffa_enter_battle': 'choose_mecha_finish'
       }

    def __init__(self, scene, name):
        super(PartFFAChooseMecha, self).__init__(scene, name, False)
        self.choose_finished_timer = None
        return

    def get_game_logic_timer(self):
        return global_data.game_mgr.get_logic_timer()

    def init_choose_mecha_ui(self):
        if not global_data.video_player.is_in_init_state():
            global_data.video_player.stop_video(ignore_cb=True)
        ui = global_data.ui_mgr.show_ui('FFAChooseMechaUI', 'logic.comsys.battle.ffa')
        ui.enter_choose_mecha()

    def choose_mecha_finish(self):
        battle = global_data.battle
        if battle and battle.choose_mecha_finish:
            battle.enter_battle()

    def clean_choose_finished_timer(self):
        self.choose_finished_timer and self.get_game_logic_timer().unregister(self.choose_finished_timer)
        self.choose_finished_timer = None
        return