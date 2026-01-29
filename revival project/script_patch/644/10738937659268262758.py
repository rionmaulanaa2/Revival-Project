# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/FlagBattle.py
from __future__ import absolute_import
from logic.entities.DeathBattle import DeathBattle
from logic.gcommon.common_const import battle_const
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool, Tuple
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB

class FlagBattle(DeathBattle):

    def init_from_dict(self, bdict):
        self.faction_to_flag_base_id = bdict.get('faction_to_flag_base_id')
        super(FlagBattle, self).init_from_dict(bdict)
        global_data.death_battle_data.update_flag_base_info(self.faction_to_flag_base_id)
        self.flag_id = bdict.get('flag_id')
        global_data.death_battle_data.set_flag_ent_id(self.flag_id)
        self.flag_reset_start_time = bdict.get('flag_reset_start_time')
        global_data.death_battle_data.set_flag_reset_start_time(self.flag_reset_start_time)
        self.flag_lock_time = bdict.get('flag_lock_time')
        global_data.death_battle_data.set_flag_lock_time(self.flag_lock_time)
        self.flag_fefresh_time = bdict.get('flag_refresh_time')
        global_data.death_battle_data.set_flag_refresh_time(self.flag_fefresh_time)

    @rpc_method(CLIENT_STUB, (Float('speed_up'),))
    def final_stage(self, speed_up):
        self.is_in_ace_state = True
        message = [{'i_type': battle_const.FLAG_BATTLE_ACE_BUFF_TIP,'set_num_func': 'set_show_percent_num','show_num': int(max(0, speed_up * 100))}, {'i_type': battle_const.FLAG_BATTLE_ACE_TIME}]
        message_type = [
         battle_const.MAIN_NODE_COMMON_INFO, battle_const.MAIN_NODE_COMMON_INFO]
        from logic.comsys.battle.Death import DeathBattleUtils
        if DeathBattleUtils.has_week_door():
            message.insert(0, {'i_type': battle_const.DEATH_DOOR_DISAPPEAR})
            message_type.insert(0, battle_const.MAIN_NODE_COMMON_INFO)
        global_data.emgr.show_battle_main_message.emit(message, message_type, True, True)
        global_data.emgr.death_into_ace_stage_event.emit()

    @rpc_method(CLIENT_STUB, (Float('flag_reset_start_time'),))
    def set_flag_reset_time(self, flag_reset_start_time):
        self.flag_reset_start_time = flag_reset_start_time
        global_data.death_battle_data.set_flag_reset_start_time(flag_reset_start_time)

    @rpc_method(CLIENT_STUB, (Float('flag_lock_start_time'),))
    def set_flag_lock_time(self, flag_lock_start_time):
        self.flag_lock_start_time = flag_lock_start_time
        global_data.death_battle_data.set_flag_lock_start_time(flag_lock_start_time)