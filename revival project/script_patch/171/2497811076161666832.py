# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/Flag2Battle.py
from __future__ import absolute_import
import six
from logic.entities.DeathBattle import DeathBattle
from logic.gcommon.common_const import battle_const
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool, Tuple
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from logic.gcommon.common_utils import battle_utils

class Flag2Battle(DeathBattle):

    def init_from_dict(self, bdict):
        self.faction_to_flag_base_id = bdict.get('faction_to_flag_base_id')
        super(Flag2Battle, self).init_from_dict(bdict)
        global_data.death_battle_data.update_flag_base_info(self.faction_to_flag_base_id)
        self.flag_id_dict = bdict.get('flag_id_dict')
        global_data.death_battle_data.set_flag_ent_id_dict(self.flag_id_dict)
        self.flag_reset_start_time = bdict.get('flag_reset_start_time')
        for k, v in six.iteritems(self.flag_reset_start_time):
            global_data.death_battle_data.set_flag_reset_start_time(v, k)

        self.flag_lock_start_time = bdict.get('flag_lock_start_time', {})
        for k, v in six.iteritems(self.flag_lock_start_time):
            global_data.death_battle_data.set_flag_lock_start_time(v, k)

        self.flag_lock_time = bdict.get('flag_lock_time')
        global_data.death_battle_data.set_flag_lock_time(self.flag_lock_time)
        self.flag_first_lock_time = bdict.get('flag_first_lock_time')
        global_data.death_battle_data.set_flag_first_lock_time(self.flag_first_lock_time)
        self.flag_fefresh_time = bdict.get('flag_refresh_time')
        global_data.death_battle_data.set_flag_refresh_time(self.flag_fefresh_time)
        self.flag_drop_refresh_time = bdict.get('flag_drop_refresh_time')
        global_data.death_battle_data.set_flag_drop_refresh_time(self.flag_drop_refresh_time)

    def on_update_group_points(self, old_group_points_dict, group_points_dict):
        TIPS_THRE = 60
        if not global_data.cam_lplayer:
            return
        else:
            msg = None
            data = group_points_dict
            first_team_over_thre = None
            for g_id in six.iterkeys(data):
                if data[g_id] >= TIPS_THRE and old_group_points_dict.get(g_id, 0) < TIPS_THRE:
                    if first_team_over_thre is None:
                        first_team_over_thre = g_id
                    else:
                        first_team_over_thre = None
                        break

            if not (global_data.player and global_data.player.logic):
                return
            my_group_id = None
            from logic.gutils import judge_utils
            if judge_utils.is_ob():
                from logic.gutils import judge_utils
                ob_unit = judge_utils.get_ob_target_unit()
                if ob_unit:
                    my_group_id = ob_unit.ev_g_group_id()
            else:
                my_group_id = global_data.player.logic.ev_g_group_id()
            if first_team_over_thre is not None and my_group_id is not None:
                if first_team_over_thre == my_group_id:
                    msg = {'i_type': battle_const.TDM_BLUE_FIRST_ARRIVE_40_POINT,'set_num_func': 'set_show_normal_point_num'
                       }
                    msg['show_num'] = TIPS_THRE
                else:
                    msg = {'i_type': battle_const.TDM_RED_FIRST_ARRIVE_40_POINT,
                       'set_num_func': 'set_show_normal_point_num'
                       }
                    msg['show_num'] = TIPS_THRE
            if msg:
                global_data.cam_lplayer.send_event('E_SHOW_MAIN_BATTLE_MESSAGE', msg, battle_const.MAIN_NODE_COMMON_INFO)
            return

    def on_receive_report_dict(self, report_dict):
        pass

    @rpc_method(CLIENT_STUB, (Float('flag_reset_start_time'), Int('faction_id')))
    def set_flag_reset_time(self, flag_reset_start_time, faction_id):
        self.flag_reset_start_time[faction_id] = flag_reset_start_time
        global_data.death_battle_data.set_flag_reset_start_time(flag_reset_start_time, faction_id)

    @rpc_method(CLIENT_STUB, (Float('flag_lock_start_time'), Int('faction_id')))
    def set_flag_lock_time(self, flag_lock_start_time, faction_id):
        self.flag_lock_start_time[faction_id] = flag_lock_start_time
        global_data.death_battle_data.set_flag_lock_start_time(flag_lock_start_time, faction_id)