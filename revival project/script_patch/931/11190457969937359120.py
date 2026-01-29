# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Death/HumanDeathBattleData.py
from __future__ import absolute_import
from common.utils import timer
from logic.comsys.battle.Death.DeathBattleData import DeathBattleData, SWIM_UI_LIST
from logic.comsys.archive import archive_key_const
import math3d

class HumanDeathBattleData(DeathBattleData):
    ALIAS_NAME = 'death_battle_data'

    def get_last_choose_weapon(self, cls_name):
        weapon_settings = global_data.achi_mgr.get_cur_user_archive_data('local_settings', {}).get('weapon_settings', {})
        death_default_weapon = weapon_settings.get('HumanDeathBattle', {})
        return weapon_settings.get(cls_name, death_default_weapon)

    def get_last_choose_down_weapon(self):
        return global_data.achi_mgr.get_general_archive_data_value(archive_key_const.KEY_LAST_HUMAN_DEATH_CHOOSE_DOWN_WEAPON, [])

    def check_pos(self):
        self.my_born_range_data = {}

        def on_check():
            if global_data.game_mode.mode and global_data.game_mode.mode.game_over:
                return
            if not (global_data.player and global_data.player.logic):
                return
            lpos = global_data.player.logic.ev_g_position()
            if not lpos:
                return
            born_data = self.get_my_born_data()
            if not born_data:
                return
            _x, _y, _z, _r, _idx, _ = born_data.data
            center_pos = math3d.vector(_x, lpos.y, _z)
            is_in_base_part = _r >= (lpos - center_pos).length * 1.0
            if not is_in_base_part:
                if self.is_in_base_part:
                    self.is_in_base_part = False
                    global_data.emgr.death_in_base_part_change.emit()
                return
            if self.is_in_base_part != is_in_base_part:
                self.is_in_base_part = is_in_base_part
                global_data.emgr.death_in_base_part_change.emit()
                self.show_swim_ui_list(SWIM_UI_LIST, True)

        self.check_pos_timer and global_data.game_mgr.get_logic_timer().unregister(self.check_pos_timer)
        self.check_pos_timer = global_data.game_mgr.get_logic_timer().register(func=on_check, mode=timer.CLOCK, interval=0.5)
        global_data.emgr.death_in_base_part_change.emit()