# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartCloneVoteMecha.py
from __future__ import absolute_import
from . import ScenePart
from common.utils import timer

class PartCloneVoteMecha(ScenePart.ScenePart):
    INIT_EVENT = {'enter_clone_vote_mecha': 'init_mecha_vote_ui',
       'clone_vote_mecha_finished': 'vote_mecha_finished'
       }

    def __init__(self, scene, name):
        super(PartCloneVoteMecha, self).__init__(scene, name, False)
        self.vote_finished_timer = None
        return

    def get_game_logic_timer(self):
        return global_data.game_mgr.get_logic_timer()

    def init_mecha_vote_ui(self):
        if not global_data.video_player.is_in_init_state():
            global_data.video_player.stop_video(ignore_cb=True)
        global_data.ui_mgr.close_ui('JudgeLoadingUI')
        ui = global_data.ui_mgr.show_ui('CloneVoteMecha', 'logic.comsys.battle.Clone')
        ui.enter_vote_mecha()

    def vote_mecha_finished(self):
        battle = global_data.battle
        if battle.mecha_vote_finished:
            self.clean_vote_finished_timer()
            self.vote_finished_timer = self.get_game_logic_timer().register(func=lambda : battle.clone_enter_battle(), mode=timer.CLOCK, interval=3, times=1)

    def clean_vote_finished_timer(self):
        self.vote_finished_timer and self.get_game_logic_timer().unregister(self.vote_finished_timer)
        self.vote_finished_timer = None
        return