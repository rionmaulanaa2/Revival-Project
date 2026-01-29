# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CImproviseMode.py
from __future__ import absolute_import
from logic.gcommon.common_utils import parachute_utils
from logic.comsys.battle import BattleUtils
from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const.battle_const import ROUND_TYPE_MECHA

class CImproviseMode(object):

    def __init__(self, map_id):
        self._map_id = map_id
        from logic.comsys.battle.Improvise.ImproviseBattleData import ImproviseBattleData
        ImproviseBattleData()
        self.process_event(True)

    def on_finalize(self):
        self.process_event(False)
        self._destroy_ui()
        global_data.improvise_battle_data.finalize()

    def _destroy_ui(self):
        global_data.ui_mgr.close_ui('ImproviseTopScoreUI')
        global_data.ui_mgr.close_ui('ImproviseBeginCountDown')
        global_data.ui_mgr.close_ui('ImproviseScoreDetailsUI')

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_init_mecha_ui': self._hide_mecha_ui,
           'on_init_state_change_ui': self._check_and_show_spectate_ui,
           'target_revive_event': self._on_target_revive
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _hide_mecha_ui(self):
        global_data.ui_mgr.hide_ui('MechaUI')

    def _check_and_show_spectate_ui(self):
        is_in_global_spectate = global_data.player and global_data.player.is_in_global_spectate()
        if is_in_global_spectate:
            global_data.ui_mgr.show_ui('ImproviseTopScoreUI', 'logic.comsys.battle.Improvise')
            if global_data.improvise_battle_data.round_type != ROUND_TYPE_MECHA:
                global_data.ui_mgr.hide_ui('StateChangeUI')

    def _on_target_revive(self):
        if global_data.cam_lplayer:
            global_data.cam_lplayer.send_event('E_TO_THIRD_PERSON_CAMERA')