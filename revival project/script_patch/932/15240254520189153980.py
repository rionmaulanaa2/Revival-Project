# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CExerciseMode.py
from __future__ import absolute_import
from logic.gcommon.common_utils import parachute_utils
from logic.gcommon import const

class CExerciseMode(object):

    def __init__(self, map_id):
        self.map_id = map_id
        self._hide_name_list = ['SOSUI', 'ScalePlateUI', 'ScalePlateUIPC', 'JudgeTeamBloodUI', 'ExerciseCommandUI', 'MechaUI', 'MechaUIPC', 'ExerciseWeaponConfUI', 'StateChangeUI', 'TeammateUI']
        self._show_name_list = []
        self.init_parameters()
        self.init_mgr()
        self.process_event(True)

    def on_finalize(self):
        self.process_event(False)
        self.destroy_ui()

    def init_parameters(self):
        pass

    def init_mgr(self):
        pass

    def destroy_ui(self):
        self.close_all_duel_ui()

    def close_all_duel_ui(self):
        global_data.ui_mgr.close_ui('ArenaWaitUI')
        global_data.ui_mgr.close_ui('ArenaApplyUI')
        global_data.ui_mgr.close_ui('ArenaConfirmUI')
        global_data.ui_mgr.close_ui('ArenaTopUI')
        global_data.ui_mgr.close_ui('ArenaEndUI')
        global_data.ui_mgr.close_ui('FFABeginCountDown')

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_battle_data': self.on_update_battle_data,
           'on_observer_parachute_stage_changed': self.on_observer_parachute_stage_changed,
           'update_battle_stage': self.on_update_battle_stage,
           'target_revive_event': self.on_target_revive,
           'scene_observed_player_setted_event': self._on_scene_observed_player_setted
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_update_battle_data(self):
        bat = global_data.player.get_battle() or global_data.player.get_joining_battle()
        if not bat:
            return
        is_in_queue = bat.is_in_queue()
        if is_in_queue:
            global_data.ui_mgr.show_ui('ArenaWaitUI', 'logic.comsys.concert')
        else:
            global_data.ui_mgr.close_ui('ArenaWaitUI')

    def _on_scene_observed_player_setted(self, player):
        self.on_target_revive()

    def on_target_revive(self):
        if global_data.cam_lplayer:
            global_data.cam_lplayer.send_event('E_TO_THIRD_PERSON_CAMERA')

    def change_ui(self):
        global_data.ui_mgr.add_blocking_ui_list(self._hide_name_list, 'duel_mode')
        global_data.ui_mgr.close_ui('MechaSummonUI')
        global_data.ui_mgr.close_ui('ExerciseEquipmentUI')

    def recover_ui(self):
        global_data.ui_mgr.remove_blocking_ui_list(self._hide_name_list, 'duel_mode')

    def is_player_in_battle_mode(self):
        from logic.gcommon.common_const import battle_const
        if not global_data.battle.is_wait_player() and global_data.battle.concert_stage == battle_const.CONCERT_FIGHT_STAGE:
            return True
        else:
            return False

    def on_update_battle_stage(self):
        if self.is_player_in_battle_mode():
            self.change_ui()
        else:
            self.recover_ui()

    def on_observer_parachute_stage_changed(self, stage):
        if stage in (parachute_utils.STAGE_SORTIE_PREPARE, parachute_utils.STAGE_SORTIE_READY, parachute_utils.STAGE_LAND):
            self.create_mode_ui()
            self.on_update_battle_stage()

    def create_mode_ui(self):
        pass