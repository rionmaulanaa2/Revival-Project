# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartMechaDeathChooseMecha.py
from __future__ import absolute_import
from . import ScenePart
from common.utils import timer

class PartMechaDeathChooseMecha(ScenePart.ScenePart):
    INIT_EVENT = {'enter_mecha_death_choose_mecha': 'init_choose_mecha_ui',
       'mecha_death_choose_mecha_finished': 'on_choose_mecha_finished'
       }

    def __init__(self, scene, name):
        super(PartMechaDeathChooseMecha, self).__init__(scene, name, False)
        self.choose_mecha_finished_timer = None
        return

    def get_game_logic_timer(self):
        return global_data.game_mgr.get_logic_timer()

    def init_choose_mecha_ui(self):
        if not global_data.video_player.is_in_init_state():
            global_data.video_player.stop_video(ignore_cb=True)
        ui = global_data.ui_mgr.show_ui('MechaDeathChooseMechaUI', 'logic.comsys.battle.MechaDeath')
        allow_mechas = None
        if hasattr(global_data.battle, 'get_allow_mechas'):
            allow_mechas = global_data.battle.get_allow_mechas()
        ui.enter_choose_mecha(allow_mechas)
        return

    def on_choose_mecha_finished(self):
        battle = global_data.battle
        if battle.is_choose_finished:
            self.clean_choose_mecha_finished_timer()
            self.choose_mecha_finished_timer = self.get_game_logic_timer().register(func=lambda : battle.mecha_death_enter_battle(), mode=timer.CLOCK, interval=3, times=1)

    def clean_choose_mecha_finished_timer(self):
        self.choose_mecha_finished_timer and self.get_game_logic_timer().unregister(self.choose_mecha_finished_timer)
        self.choose_mecha_finished_timer = None
        return