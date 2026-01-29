# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/NBombSurvivalBattle.py
from __future__ import absolute_import
from logic.entities.SurvivalBattle import SurvivalBattle
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool, Tuple
from logic.gcommon.common_const import battle_const
from logic.comsys.battle.NBomb import nbomb_utils

class NBombSurvivalBattle(SurvivalBattle):

    def init_from_dict(self, bdict):
        super(NBombSurvivalBattle, self).init_from_dict(bdict)
        nbomb_core_soul_hold = bdict.get('nbomb_core_soul_hold', {})
        nbomb_core_group_hold = bdict.get('nbomb_core_group_hold', {})
        nbomb_explode_timestamp = bdict.get('nbomb_explode_timestamp', 0)
        nbomb_group_id = bdict.get('nbomb_group_id', 0)
        soul_ids = bdict.get('nbomb_soul_ids', [])
        nbomb_exploded = bdict.get('nbomb_exploded', False)
        nbomb_destroyed = bdict.get('nbomb_destroyed', False)
        is_spawned = bdict.get('nbomb_core_spawned', False)
        self_group_id = bdict.get('loading_group_id')
        basic_info = {'exploded': nbomb_exploded,
           'destroyed': nbomb_destroyed,
           'group_id': self_group_id
           }
        self.on_update_nbomb_basic(basic_info)
        if nbomb_exploded or nbomb_destroyed:
            return
        else:
            nbomb_confirm_timestamp = bdict.get('nbomb_confirm_timestamp', 0)
            nbomb_confirm_soul_id = bdict.get('nbomb_confirm_soul_id', None)
            ret = nbomb_confirm_soul_id and nbomb_confirm_timestamp
            self.on_nbomb_install_evt(nbomb_confirm_soul_id, nbomb_confirm_timestamp, ret)
            self.on_update_nbomb_core_info(nbomb_core_soul_hold, nbomb_core_group_hold)
            self.on_update_nbomb_installed(nbomb_explode_timestamp, nbomb_group_id, soul_ids)
            self.on_update_nbomb_core_spawned(is_spawned)
            return

    def on_update_nbomb_core_spawned(self, nbomb_core_spawned):
        if not global_data.nbomb_battle_data:
            return
        old_is_spawned = global_data.nbomb_battle_data.is_nbomb_core_spawned
        global_data.nbomb_battle_data.set_nbomb_core_spawned(nbomb_core_spawned)
        if nbomb_utils.is_data_ready():
            global_data.emgr.nbomb_update_ui_show.emit()
        if nbomb_core_spawned and not old_is_spawned:
            global_data.emgr.scene_poison_updated_event.emit()

    def on_update_nbomb_core_info(self, d_core_info, d_group_core_info):
        if not global_data.nbomb_battle_data:
            return
        global_data.nbomb_battle_data.update_nbomb_core_info(d_core_info, d_group_core_info)

    def on_update_nbomb_installed(self, init_timestamp, nbomb_group_id, soul_ids):
        if not global_data.nbomb_battle_data:
            return
        global_data.nbomb_battle_data.update_nbomb_installed(init_timestamp, nbomb_group_id, soul_ids)

    def on_nbomb_install_evt(self, _player_id, _finish_timestamp, is_confirm):
        if not global_data.nbomb_battle_data:
            return
        if is_confirm:
            global_data.nbomb_battle_data.start_install_nbomb(_player_id, _finish_timestamp)
        else:
            global_data.nbomb_battle_data.stop_instal_nbomb()

    def on_update_nbomb_basic(self, basic_info):
        if global_data.nbomb_battle_data:
            global_data.nbomb_battle_data.on_update_nbomb_basic(basic_info)

    @rpc_method(CLIENT_STUB, (Dict('d_soul_core_info'), Dict('d_group_core_info')))
    def sync_nbomb_core_hold_info(self, d_soul_core_info, d_group_core_info):
        self.on_update_nbomb_core_info(d_soul_core_info, d_group_core_info)
        global_data.emgr.nbomb_core_got_status_our_group.emit()

    @rpc_method(CLIENT_STUB, (Int('i_bomb_status'),))
    def sync_nbomb_status(self, i_bomb_status):
        pass

    @rpc_method(CLIENT_STUB, (Float('init_timestamp'), Int('nbomb_group_id'), List('soul_ids'), Tuple('bomb_pos')))
    def notify_start_nbomb_ret(self, init_timestamp, nbomb_group_id, soul_ids, bomb_pos):
        self.on_update_nbomb_installed(init_timestamp, nbomb_group_id, soul_ids)
        global_data.emgr.nbomb_update_ui_show.emit({'is_placed_nbomb_cb': True})
        global_data.emgr.nbomb_show_tips.emit(battle_const.NBOMB_TIP_NBOMB_START)
        global_data.emgr.nbomb_show_map_overview.emit({'target_pos': bomb_pos})

    @rpc_method(CLIENT_STUB, (Bool('ret'), Float('timestamp'), Uuid('soul_id')))
    def notify_nbomb_confirm_ret(self, ret, timestamp, soul_id):
        self.on_nbomb_install_evt(soul_id, timestamp, ret)

    @rpc_method(CLIENT_STUB, ())
    def notify_get_all_nbomb_core(self):
        pass

    @rpc_method(CLIENT_STUB, (Bool('is_exploded'),))
    def notify_nbomb_exploded(self, is_exploded):
        if not is_exploded:
            return
        basic_info = {'exploded': True}
        self.on_update_nbomb_basic(basic_info)
        global_data.emgr.nbomb_show_tips.emit(battle_const.NBOMB_TIP_NBOMB_EXPLODE)

    @rpc_method(CLIENT_STUB, (Bool('is_destroyed'),))
    def notify_nbomb_destroyed(self, is_destroyed):
        if not global_data.nbomb_battle_data:
            return
        old_nbomb_destroyed = global_data.nbomb_battle_data.nbomb_destroyed
        basic_info = {'destroyed': is_destroyed
           }
        self.on_update_nbomb_basic(basic_info)
        if not old_nbomb_destroyed and is_destroyed:
            global_data.emgr.nbomb_show_tips.emit(battle_const.NBOMB_TIP_NBOMB_DESTROY)
            global_data.emgr.nbomb_play_sky_resume_sfx.emit()
            global_data.emgr.nbomb_clear_war.emit()

    @rpc_method(CLIENT_STUB, (Str('tip_type'), Dict('tip_data')))
    def show_nbomb_tips(self, tip_type, tip_data):
        global_data.emgr.nbomb_show_tips.emit(tip_type, tip_data)

    @rpc_method(CLIENT_STUB, (Int('player_num'),))
    def update_player_num(self, player_num):
        self.alive_player_num = player_num
        is_exploded = global_data.nbomb_battle_data and global_data.nbomb_battle_data.nbomb_exploded
        if not is_exploded:
            global_data.emgr.update_alive_player_num_event.emit(player_num)

    @rpc_method(CLIENT_STUB, (Bool('is_spawned'),))
    def spawn_nbomb_items(self, is_spawned):
        self.on_update_nbomb_core_spawned(is_spawned)

    def recruit_valid(self):
        return False