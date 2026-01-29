# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/NBomb/NBombBattleData.py
from __future__ import absolute_import
import six
import six_ex
from common.framework import Singleton
from logic.comsys.battle.NBomb.NBombBattleDefines import POWER_CORE_ID, SPACE_CORE_ID, SPEED_CORE_ID, NBOMB_CORE_LEN, POWER_CORE_ID_LST

class NBombBattleData(Singleton):
    ALIAS_NAME = 'nbomb_battle_data'

    def init(self):
        self.nbomb_exploded = False
        self.nbomb_destroyed = False
        self.reset_parameters()
        self.process_event(True)

    def reset_parameters(self):
        self.is_ready_state = False
        self.self_group_id = 0
        self.is_nbomb_core_spawned = False
        self.nbomb_core_info = {}
        self.nbomb_group_core_info = {}
        self.nbomb_core_enemy_info = {}
        self.bomb_explosion_time = 0
        self.my_team_core_info = {POWER_CORE_ID: 0,
           SPACE_CORE_ID: 0,
           SPEED_CORE_ID: 0
           }
        self.core_own_info = {POWER_CORE_ID: 0,
           SPACE_CORE_ID: 0,
           SPEED_CORE_ID: 0
           }
        self.bomb_install_time = 0
        self.try_install_player_id = 0
        self.succeed_install_group_id = 0
        self.succeed_install_soul_ids = []

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_player_inited_event': self._on_update_groupmate,
           'scene_camera_player_setted_event': self._on_update_groupmate
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize(self):
        self.process_event(False)
        self.reset_parameters()

    def on_update_nbomb_basic(self, basic_info):
        if basic_info.get('exploded', None) is not None:
            self.nbomb_exploded = basic_info.get('exploded', None)
        if basic_info.get('destroyed', None) is not None:
            self.nbomb_destroyed = basic_info.get('destroyed', None)
        if basic_info.get('group_id', None) is not None:
            self.self_group_id = basic_info.get('group_id', None)
        return

    def get_nbomb_core_info(self):
        return self.nbomb_core_info

    def get_nbomb_core_soul_ids(self):
        return list(self.nbomb_core_info.keys())

    def update_nbomb_core_info(self, info, d_group_core_info):
        self.nbomb_core_info = info
        self.nbomb_group_core_info = d_group_core_info
        global_data.emgr.nbomb_core_got_status.emit()
        if global_data.cam_lplayer:
            self._on_update_groupmate(global_data.cam_lplayer)

    def _on_update_groupmate(self, lplayer=None):
        if not global_data.cam_lplayer:
            return
        else:
            info = self.nbomb_core_info
            old_core_own_info = self.core_own_info
            self.my_team_core_info = {POWER_CORE_ID: 0,
               SPACE_CORE_ID: 0,
               SPEED_CORE_ID: 0
               }
            new_core_own_info = {POWER_CORE_ID: 0,
               SPACE_CORE_ID: 0,
               SPEED_CORE_ID: 0
               }
            self.nbomb_core_enemy_info = {}
            for player_id in six.iterkeys(info):
                if player_id:
                    for _, core_config_id in six.iteritems(info[player_id]):
                        new_core_own_info[core_config_id] = player_id
                        if global_data.cam_lplayer.ev_g_is_groupmate(player_id):
                            self.my_team_core_info[core_config_id] = player_id
                        else:
                            if player_id not in self.nbomb_core_enemy_info:
                                self.nbomb_core_enemy_info[player_id] = []
                            self.nbomb_core_enemy_info[player_id].append(core_config_id)

            is_exchange = False
            core_exchange_info = []
            for core_config_id in POWER_CORE_ID_LST:
                if new_core_own_info.get(core_config_id) and not old_core_own_info.get(core_config_id):
                    core_exchange_info.append(core_config_id)
                    is_exchange = True

            self.core_own_info = new_core_own_info
            global_data.emgr.nbomb_core_got_status_our_group.emit(core_exchange_info if is_exchange else None)
            return

    def get_nbomb_core_enemy_info(self):
        return self.nbomb_core_enemy_info

    def get_own_team_core_info(self):
        return self.my_team_core_info

    def get_own_core_cnt(self):
        own_cnt = 0
        for player_id in six.itervalues(self.my_team_core_info):
            if player_id:
                own_cnt += 1

        return own_cnt

    def is_group_collect_core(self):
        own_cnt = self.get_own_core_cnt()
        return own_cnt > 0

    def is_collect_all_core(self):
        own_cnt = self.get_own_core_cnt()
        return own_cnt >= NBOMB_CORE_LEN

    def set_nbomb_core_spawned(self, _is_nbomb_core_spawned):
        self.is_nbomb_core_spawned = _is_nbomb_core_spawned

    def start_install_nbomb(self, _player_id, _finish_time):
        self.bomb_install_time = _finish_time
        self.try_install_player_id = _player_id
        global_data.emgr.nbomb_start_install.emit()

    def stop_instal_nbomb(self):
        self.bomb_install_time = 0
        self.try_install_player_id = 0
        global_data.emgr.nbomb_stop_install.emit()

    def update_nbomb_installed(self, _bomb_explosion_time, _nbomb_group_id, _soul_ids):
        self.bomb_explosion_time = _bomb_explosion_time
        self.succeed_install_group_id = _nbomb_group_id
        self.succeed_install_soul_ids = _soul_ids
        global_data.emgr.nbomb_update_explosion.emit(_bomb_explosion_time, _nbomb_group_id, _soul_ids)

    def get_nbomb_installed_soul_ids(self):
        return self.succeed_install_soul_ids

    def is_install_nbomb(self):
        no_destroyed = self.nbomb_destroyed == False
        no_exploded = self.nbomb_exploded == False
        return self.bomb_explosion_time != 0 and no_destroyed and no_exploded

    def get_nbomb_cd_timestamp(self):
        return self.bomb_explosion_time

    def get_nbomb_install_timestamp(self):
        return self.bomb_install_time

    def get_nbomb_install_player_id(self):
        return self.try_install_player_id

    def get_self_group_id(self):
        if global_data.cam_lplayer:
            return global_data.cam_lplayer.ev_g_group_id()
        return self.self_group_id

    def is_self_group_install_nbomb(self):
        return self.get_self_group_id() == self.succeed_install_group_id