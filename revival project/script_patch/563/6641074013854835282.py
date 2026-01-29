# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/ArmRaceBattle.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import List, Dict, Int, Float, Bool
from logic.gcommon.common_const import battle_const
from logic.entities.Battle import Battle
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gcommon import time_utility as tutils

class ArmRaceBattle(Battle):

    def __init__(self, entityid):
        super(ArmRaceBattle, self).__init__(entityid)

    def enter_battle(self):
        super(ArmRaceBattle, self).init_from_dict(self.battle_bdict)

    def init_from_dict(self, bdict):
        self.battle_bdict = bdict
        self.sync_battle_time()
        self.area_id = bdict.get('area_id')
        self.map_id = bdict.get('map_id')
        self.start_suicide_result((bdict.get('suicide_timestamp', 0),))
        self.rechoose_mecha_flag = bdict.get('rechoose_mecha_flag', False)
        self.armrace_level_weapom = bdict.get('armrace_level_weapom')
        self.enter_battle()

    def sync_battle_time(self):
        battle_srv_time = self.battle_bdict.get('battle_srv_time', None)
        if battle_srv_time and tutils.TYPE_BATTLE not in tutils.g_success_flag:
            tutils.on_sync_time(tutils.TYPE_BATTLE, battle_srv_time)
        return

    def boarding_movie_data(self):
        return None

    def get_armrace_level_weapom(self):
        return self.armrace_level_weapom

    @rpc_method(CLIENT_STUB, (List('group_rank_data'),))
    def update_group_points(self, group_rank_data):
        global_data.armrace_battle_data.set_group_score_data(group_rank_data)

    @rpc_method(CLIENT_STUB, (List('rank_data'),))
    def reply_rank_data(self, rank_data):
        global_data.armrace_battle_data.set_score_details_data(rank_data)

    @rpc_method(CLIENT_STUB, (Float('settle_timestamp'),))
    def update_settle_timestamp(self, settle_timestamp):
        self.settle_timestamp = settle_timestamp
        global_data.armrace_battle_data.set_settle_timestamp(settle_timestamp)

    @rpc_method(CLIENT_STUB, (Float('settle_timestamp'),))
    def update_battle_data(self, settle_timestamp):
        self.update_settle_timestamp((settle_timestamp,))

    @rpc_method(CLIENT_STUB, (Int('group_id'), Dict('soul_data')))
    def notify_top_group_info(self, group_id, soul_data):
        global_data.armrace_battle_data.notify_top_group_info(group_id, soul_data)

    @rpc_method(CLIENT_STUB, (Bool('result'),))
    def start_combat_result(self, result):
        if result:
            global_data.ui_mgr.close_ui('DeathPlayBackUI')

    @rpc_method(CLIENT_STUB, (Dict('stage_dict'),))
    def prepare_stage(self, stage_dict):
        prepare_timestamp = stage_dict.get('prepare_timestamp')
        if prepare_timestamp:
            self.battle_bdict['prepare_timestamp'] = prepare_timestamp
        super(ArmRaceBattle, self).prepare_stage((stage_dict,))

    @rpc_method(CLIENT_STUB, (Dict('stage_dict'),))
    def fight_stage(self, stage_dict):
        super(ArmRaceBattle, self).fight_stage((stage_dict,))

    @rpc_method(CLIENT_STUB, (Float('final_prate'),))
    def final_stage(self, final_prate):
        self.is_in_ace_state = True
        global_data.emgr.show_battle_main_message.emit({'i_type': battle_const.ARMRACE_ACE_TIME}, battle_const.MAIN_NODE_COMMON_INFO)

    def start_combat(self):
        self.call_soul_method('start_combat', ())

    @rpc_method(CLIENT_STUB, (Int('level'),))
    def armrace_level_up(self, level):
        msg = {'i_type': battle_const.ARMRACE_LEVEL_UP,'set_attr_dict': {'node_name': 'lab_level','func_name': 'SetString',
                             'args': (
                                    get_text_by_id(17248).format(level),)
                             }
           }
        global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)

    @rpc_method(CLIENT_STUB, (Int('level'), Dict('kill_info')))
    def armrace_headhit_notify(self, level, kill_info):
        reply_data = kill_info.get('reply_data', {})
        killer_info = kill_info.get('killer_info', {})
        killer_hit = kill_info.get('killer_hit', [])
        role_name = killer_info.get('role_name', '\xe6\x9c\xaa\xe7\x9f\xa5')
        msg = ''
        if killer_hit:
            item_id = killer_hit[-1][1]
            weapon_type = confmgr.get('hit_hint', str(item_id), default={}).get('iWeaponType', '')
            weapon_name = item_utils.get_item_name(weapon_type)
            msg = '\xe4\xbd\xa0\xe8\xa2\xab{0}\xe7\x94\xa8{1}\xe7\x88\x86\xe5\xa4\xb4\xe7\x8b\x99\xe5\x87\xbb'.format(role_name, weapon_name)
        msg = {'i_type': battle_const.ARMRACE_LEVEL_DOWN,'set_attr_dict': [
                           {'node_name': 'lab_info','func_name': 'SetString',
                              'args': (
                                     msg,)
                              },
                           {'node_name': 'lab_level','func_name': 'SetString',
                              'args': (
                                     str(level),)
                              }]
           }
        global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)

    @rpc_method(CLIENT_STUB, ())
    def armrace_stop_fire(self):
        if global_data.cam_lplayer:
            player = global_data.cam_lplayer
            player.send_event('E_CTRL_ACCUMULATE', False)
            player.send_event('E_ATTACK_END')
            if global_data.is_allow_sideways:
                player.send_event('E_END_FIRE_ROCKER')
            else:
                player.send_event('E_STOP_AUTO_FIRE')
            player.send_event('E_QUIT_AIM')

    @rpc_method(CLIENT_STUB, (Int('level'), Int('now_level_kill'), Bool('level_up')))
    def update_armrace_level(self, level, now_level_kill, level_up):
        global_data.armrace_battle_data.set_armrace_level(level, now_level_kill, level_up)

    def start_suicide(self):
        self.call_soul_method('start_suicide', ())

    @rpc_method(CLIENT_STUB, (Float('suicide_timestamp'),))
    def start_suicide_result(self, suicide_timestamp):
        self.suicide_timestamp = suicide_timestamp
        global_data.emgr.update_death_come_home_time.emit()

    def get_suicide_timestamp(self):
        return self.suicide_timestamp