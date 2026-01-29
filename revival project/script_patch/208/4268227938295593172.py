# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/DeathBattle.py
from __future__ import absolute_import
import six
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool, Tuple
from logic.gcommon.common_const import battle_const
from logic.entities.Battle import Battle
from logic.gcommon.common_utils import battle_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
import math3d
from logic.gcommon import const
from collections import defaultdict
from logic.gcommon.common_const import ui_operation_const as uoc

class DeathBattle(Battle):

    def init_from_dict(self, bdict, is_change_weapon=True):
        self.settle_timestamp = 0
        weapon_dict = bdict.get('weapon_dict', {})
        weapon_dict.pop(const.PART_WEAPON_POS_MAIN_DF, None)
        super(DeathBattle, self).init_from_dict(bdict)
        battle_data = global_data.death_battle_data
        self.area_id = bdict.get('area_id')
        battle_data.set_area_id(str(self.area_id))
        is_change = battle_data.save_select_weapon_data(weapon_dict, self.__class__.__name__) and is_change_weapon
        is_change and self.set_combat_weapons(battle_data.get_select_weapon_data())
        spawn_rebirth_dict = bdict.get('spawn_rebirth_dict', {})
        battle_data.update_spawn_rebirth_data(spawn_rebirth_dict)
        self._settle_point = bdict.get('settle_point', 50)
        self.start_suicide_result((bdict.get('suicide_timestamp', 0),))
        self.all_battle_flag = bdict.get('all_battle_flag', [])
        self.is_open_aicollectlog = bdict.get('is_open_aicollectlog', False)
        battle_data.rogue_gift_candidates = bdict.get('rogue_gift_candidates', {})
        battle_data.selected_rogue_gifts.update(bdict.get('selected_rogue_gifts', {}))
        battle_data.rogue_distribute_times = bdict.get('rogue_distribute_times', [])
        battle_data.enable_out_base_rogue = bdict.get('enable_out_base_rogue', False)
        battle_data.refresh_conf_list = bdict.get('rogue_refresh_conf_list')
        battle_data.rogue_refresh_times = bdict.get('rogue_refresh_times', defaultdict(int))
        battle_data.max_refresh_time = bdict.get('max_refresh_time')
        if global_data.need_runtime_profile:
            from logic.gutils.profile_utils import RuntimeProfiler
            RuntimeProfiler().start_pro_timer()
        return

    def destroy(self, clear_cache=True):
        super(DeathBattle, self).destroy(clear_cache)
        if global_data.runtime_profiler:
            global_data.runtime_profiler.end_pro_timer()

    def boarding_movie_data(self):
        from data.battle_trans_anim import Getmecha_boarding_tdm
        return Getmecha_boarding_tdm()

    def on_receive_report_dict(self, report_dict):
        if not global_data.cam_lplayer:
            return
        else:
            msg = None
            killer_id, injured_id, _ = battle_utils.parse_battle_report_death(report_dict)
            is_mecha = False
            show_points = 0
            if killer_id:
                is_my_side = global_data.cam_lplayer and global_data.cam_lplayer.ev_g_is_campmate_by_eid(killer_id)
                if killer_id == global_data.cam_lplayer.id:
                    msg = {'i_type': battle_const.MAIN_KOTH_KILL_POINT,'icon_path': 'gui/ui_res_2/battle/notice/icon_msg_kill.png'
                       }
                    msg['show_num'] = report_dict.get('points', 0)
                if is_my_side:
                    show_points = report_dict.get('points', 0)
            mecha_killer_id, mecha_injured_id = battle_utils.parse_battle_report_mecha_death(report_dict)
            if mecha_killer_id:
                is_my_side = global_data.cam_lplayer and global_data.cam_lplayer.ev_g_is_campmate_by_eid(mecha_killer_id)
                if mecha_killer_id == global_data.cam_lplayer.id:
                    msg = {'i_type': battle_const.MAIN_KOTH_KILL_MECHA_POINT}
                    msg['show_num'] = report_dict.get('points', 0)
                if is_my_side:
                    show_points = report_dict.get('points', 0)
                    is_mecha = True
            if msg:
                global_data.cam_lplayer.send_event('E_SHOW_MAIN_BATTLE_MESSAGE', msg, battle_const.MAIN_NODE_POINT)
            if show_points:
                global_data.emgr.show_battle_points.emit(is_mecha, show_points)
            return

    def get_move_range(self):
        born_data = global_data.game_mode.get_born_data()
        move_range = born_data[str(self.area_id)].get('move_range', {})
        return move_range

    def get_settle_point(self):
        return self._settle_point

    @rpc_method(CLIENT_STUB, (Float('settle_timestamp'), List('born_point_list'), Dict('group_born_dict'), Dict('group_points_dict'), Dict('selected_combat_weapons')))
    def update_battle_data(self, settle_timestamp, born_point_list, group_born_dict, group_points_dict, selected_combat_weapons):
        self._update_battle_data(settle_timestamp, born_point_list, group_born_dict, group_points_dict, selected_combat_weapons)

    def _update_battle_data(self, settle_timestamp, born_point_list, group_born_dict, group_points_dict, selected_combat_weapons):
        self.update_settle_timestamp((settle_timestamp,))
        self.update_born_point((born_point_list, group_born_dict))
        for group_id in six.iterkeys(group_born_dict):
            if group_id not in group_points_dict:
                group_points_dict[group_id] = 0

        self.update_group_points((group_points_dict,))
        if selected_combat_weapons:
            global_data.death_battle_data.set_select_weapon_data(selected_combat_weapons)

    @rpc_method(CLIENT_STUB, (Float('settle_timestamp'),))
    def update_settle_timestamp(self, settle_timestamp):
        self.settle_timestamp = settle_timestamp
        global_data.death_battle_data.set_settle_timestamp(settle_timestamp)

    @rpc_method(CLIENT_STUB, (List('born_point_list'), Dict('group_born_dict')))
    def update_born_point(self, born_point_list, group_born_dict):
        global_data.death_battle_data and global_data.death_battle_data.update_born_point(group_born_dict, born_point_list)

    @rpc_method(CLIENT_STUB, (Dict('group_points_dict'),))
    def update_group_points(self, group_points_dict):
        if global_data.death_battle_data:
            old_group_points_dict = dict(global_data.death_battle_data.get_group_score_data())
        else:
            old_group_points_dict = {}
        global_data.death_battle_data and global_data.death_battle_data.update_group_score_data(group_points_dict)
        if old_group_points_dict:
            self.on_update_group_points(old_group_points_dict, group_points_dict)

    def on_update_group_points(self, old_group_points_dict, group_points_dict):
        TIPS_THRE = battle_const.TDM_FIRST_POINTS_TIPS_THRE
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

    @rpc_method(CLIENT_STUB, (Dict('rank_data'),))
    def reply_rank_data(self, rank_data):
        if global_data.death_battle_data:
            global_data.death_battle_data.update_score_details_data(rank_data)

    @rpc_method(CLIENT_STUB, (Dict('all_group_status_dict'),))
    def update_all_group_status(self, all_group_status_dict):
        if global_data.death_battle_data:
            global_data.death_battle_data.update_all_group_status(all_group_status_dict)

    @rpc_method(CLIENT_STUB, (Float('final_prate'), Float('final_srate')))
    def final_stage(self, final_prate, final_srate):
        self.is_in_ace_state = True
        message = []
        if final_srate != 0:
            message = [{'i_type': battle_const.TDM_THREE_TIMES_POINT_NEW,'set_num_func': 'set_show_percent_num','num_list': [int(max(0, final_prate * 100 - 100)), int(final_srate * 100)]}, {'i_type': battle_const.SECOND_ACE_TIME_NEW}]
        else:
            message = [{'i_type': battle_const.TDM_THREE_TIMES_POINT,'set_num_func': 'set_show_percent_num','show_num': int(max(0, final_prate - 1) * 100)}, {'i_type': battle_const.SECOND_ACE_TIME}]
        message_type = [
         battle_const.MAIN_NODE_COMMON_INFO, battle_const.MAIN_NODE_COMMON_INFO]
        from logic.comsys.battle.Death import DeathBattleUtils
        if DeathBattleUtils.has_week_door():
            message.insert(0, {'i_type': battle_const.DEATH_DOOR_DISAPPEAR})
            message_type.insert(0, battle_const.MAIN_NODE_COMMON_INFO)
        global_data.emgr.show_battle_main_message.emit(message, message_type, True, True)
        global_data.emgr.death_into_ace_stage_event.emit()

    def start_suicide(self):
        self.call_soul_method('start_suicide', ())

    @rpc_method(CLIENT_STUB, (Float('suicide_timestamp'),))
    def start_suicide_result(self, suicide_timestamp):
        self.suicide_timestamp = suicide_timestamp
        global_data.emgr.update_death_come_home_time.emit()
        if not global_data.cam_lplayer:
            return
        msg = {'i_type': battle_const.TDM_COME_HOME,'content_txt': get_text_by_id(19475)}
        global_data.cam_lplayer.send_event('E_SHOW_MAIN_BATTLE_MESSAGE', msg, battle_const.MAIN_NODE_COMMON_INFO)

    def get_suicide_timestamp(self):
        return self.suicide_timestamp

    @rpc_method(CLIENT_STUB, (Str('tele_role'), Tuple('tele_pos')))
    def suicide_teleport_all(self, tele_role, tele_pos):
        from logic.gutils import granbelm_utils
        sfx_path = granbelm_utils.get_tele_sfx_path(2, tele_role, 1)
        sfx_pos = math3d.vector(tele_pos[0], tele_pos[1], tele_pos[2])
        global_data.sfx_mgr.create_sfx_in_scene(sfx_path, sfx_pos)

    @rpc_method(CLIENT_STUB, ())
    def battle_revive(self):
        pass

    def start_combat(self):
        self.call_soul_method('start_combat', ())

    @rpc_method(CLIENT_STUB, (Bool('result'),))
    def start_combat_result(self, result):
        if result:
            global_data.ui_mgr.close_ui('DeathPlayBackUI')

    def set_combat_weapons(self, weapon_dict):
        self.call_soul_method('set_combat_weapons', (weapon_dict,))

    @rpc_method(CLIENT_STUB, (Int('install_index'),))
    def module_auto_install(self, install_index):
        self.on_module_auto_install(install_index)

    def on_module_auto_install(self, install_index):
        info_dict = {1: (
             'gui/ui_res_2/item/9913.png', '#SB', get_text_by_id(17014), 17017),
           2: (
             'gui/ui_res_2/item/9908.png', '#SP', get_text_by_id(17015), 17017),
           3: (
             'gui/ui_res_2/item/9911.png', '#SO', get_text_by_id(17016), 17018)
           }
        if install_index not in info_dict:
            return
        sprite_path, color_str, name, content_id = info_dict.get(install_index)
        msg = {'i_type': battle_const.TDM_ABOUT_TO_GET_MODULE_UPGRADE,
           'icon_path': sprite_path,
           'content_txt': get_text_by_id(content_id, {'color': color_str,'module_name': name})
           }
        if msg and global_data.cam_lplayer:
            global_data.cam_lplayer.send_event('E_SHOW_MAIN_BATTLE_MESSAGE', msg, battle_const.MAIN_NODE_COMMON_INFO)

    @rpc_method(CLIENT_STUB, (Uuid('entity_id'), Int('achievement_id'), Dict('extra_info')))
    def on_player_get_achievement(self, entity_id, achievement_id, extra_info):
        from mobile.common.EntityManager import EntityManager
        target = EntityManager.getentity(entity_id)
        if target and target.logic:
            desc_text_id = confmgr.get('battle_achieve_data', str(achievement_id), default={}).get('desc_text_id')
            txt = ' '.join([target.logic.ev_g_char_name(), get_text_by_id(desc_text_id)])
            msg = {'i_type': battle_const.TDM_ACHIEVE_TIPS,'content_txt': txt}
            global_data.cam_lplayer.send_event('E_SHOW_MAIN_BATTLE_MESSAGE', msg, battle_const.MAIN_NODE_COMMON_INFO)

    @rpc_method(CLIENT_STUB, (Uuid('entity_id'), Dict('state_info')))
    def update_player_state_info(self, entity_id, state_info):
        pass

    @rpc_method(CLIENT_STUB, (List('prompt_id_list'), Str('eid'), Str('name'), Dict('short_kill_info')))
    def on_kill_prompt(self, prompt_id_list, eid, name, short_kill_info):
        from mobile.common.EntityManager import EntityManager
        from logic.gcommon.item.item_const import FASHION_POS_SUIT
        cam_lctarget = global_data.cam_lctarget
        death_id = short_kill_info.get('player_eid', 0)
        death_player = EntityManager.getentity(death_id)
        killer_type = short_kill_info.get('killer_type', 0)
        from logic.gcommon.ctypes.FightData import FD_MAKER_MECHA
        if killer_type == FD_MAKER_MECHA:
            killer_is_mecha = True
            killer_skin = short_kill_info.get('killer_mecha_fashion', {}).get(FASHION_POS_SUIT)
        else:
            killer_id = short_kill_info.get('killer_id')
            killer = EntityManager.getentity(killer_id)
            fashion = (killer.logic.ev_g_fashion() if killer and killer.logic else {}) or {}
            killer_is_mecha = False
            killer_skin = fashion.get(FASHION_POS_SUIT)
        if not killer_skin:
            return
        if short_kill_info.get('kill_mecha', False):
            death_is_mecha = True
            death_skin = short_kill_info.get('mecha_fasion', {}).get(FASHION_POS_SUIT)
        else:
            death_fashion = (death_player.logic.ev_g_fashion() if death_player and death_player.logic else {}) or {}
            death_is_mecha = False
            death_skin = death_fashion.get(FASHION_POS_SUIT)
        if not death_skin:
            return
        for prompt_id in prompt_id_list:
            if cam_lctarget and death_player and death_player.logic:
                if cam_lctarget.ev_g_is_campmate(death_player.logic.ev_g_camp_id()):
                    frd_mecha_id = (
                     death_is_mecha, death_skin)
                    eny_mecha_id = (killer_is_mecha, killer_skin)
                    frd_is_killer = False
                else:
                    frd_mecha_id = (
                     killer_is_mecha, killer_skin)
                    eny_mecha_id = (death_is_mecha, death_skin)
                    frd_is_killer = True
                if frd_mecha_id and eny_mecha_id:
                    msg = battle_utils.get_death_kill_prompt_msg(prompt_id, frd_mecha_id, eny_mecha_id, frd_is_killer, name)
                    global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)

    @rpc_method(CLIENT_STUB, (Int('born_idx'), Dict('battle_flag')))
    def update_all_battle_flag(self, born_idx, battle_flag):
        self.all_battle_flag.append((born_idx, battle_flag))

    def get_battle_flag(self):
        return self.all_battle_flag

    @rpc_method(CLIENT_STUB, (Dict('msg'),))
    def group_message(self, msg):
        if global_data.player and global_data.player.get_setting_2(uoc.BLOCK_ALL_MSG_KEY):
            return
        unit_id = msg['id']
        text_block_mate = global_data.player.logic.ev_g_text_block_mate()
        if unit_id in text_block_mate:
            return
        unit_name = msg['char_name']
        msg['msg']['head_frame'] = msg['head_frame']
        msg['msg']['role_id'] = msg['role_id']
        global_data.emgr.add_battle_group_msg_event.emit(unit_id, unit_name, msg)
        if global_data.player and global_data.player.logic:
            global_data.player.logic.send_event('E_ADD_GROUP_HISTORY_MSG', unit_id, unit_name, msg['msg'])

    @rpc_method(CLIENT_STUB, (Int('spawn_id'), Int('faction_id'), Float('rebirth_ts')))
    def update_spawn_rebirth(self, spawn_id, faction_id, rebirth_ts):
        global_data.death_battle_data.update_spawn_rebirth_data({spawn_id: (faction_id, rebirth_ts)})
        global_data.emgr.update_spawn_rebirth_data_event.emit([spawn_id])

    @rpc_method(CLIENT_STUB, (Dict('battle_rogue_gifts'),))
    def death_rogue_update(self, battle_rogue_gifts):
        if global_data.death_battle_data:
            global_data.death_battle_data.rogue_gift_candidates = battle_rogue_gifts
        global_data.emgr.rogue_gift_update_candidates.emit()

    @rpc_method(CLIENT_STUB, (Bool('enable_out_base_rogue'),))
    def clear_rogue(self, enable_out_base_rogue):
        battle_data = global_data.death_battle_data
        battle_data.rogue_gift_candidates = {}
        battle_data.selected_rogue_gifts = defaultdict(dict)
        battle_data.enable_out_base_rogue = enable_out_base_rogue
        battle_data.rogue_refresh_times = defaultdict(int)
        global_data.ui_mgr.close_ui('DeathRogueChooseUI')
        ui = global_data.ui_mgr.get_ui('RogueChooseBtnUI')
        ui and ui.hide()

    @rpc_method(CLIENT_STUB, (Uuid('eid'), Int('rogue_key'), Int('rogue_id')))
    def death_rogue_select(self, eid, rogue_key, rogue_id):
        if not global_data.death_battle_data:
            return
        global_data.death_battle_data.selected_rogue_gifts[eid][rogue_key] = rogue_id
        global_data.emgr.rogue_gift_update_select.emit(eid, rogue_key)

    @rpc_method(CLIENT_STUB, (Int('pre_notify_time'),))
    def pre_rogue_stage(self, pre_notify_time):
        msg = {'i_type': battle_const.TDM_PRE_NOTIFY_ROGUE_GIFT}
        global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)

    @rpc_method(CLIENT_STUB, (Dict('selected_rogue_gifts'),))
    def death_rogue_update_select(self, selected_rogue_gifts):
        global_data.death_battle_data.selected_rogue_gifts.update(selected_rogue_gifts)

    @rpc_method(CLIENT_STUB, (Uuid('soul_id'), Int('time_key'), List('candidates'), Int('refresh_times')))
    def update_refresh_gifts(self, soul_id, time_key, candidates, refresh_times):
        battle_data = global_data.death_battle_data
        if not battle_data:
            return
        if soul_id not in battle_data.rogue_gift_candidates:
            battle_data.rogue_gift_candidates[soul_id] = defaultdict(list)
        battle_data.rogue_gift_candidates[soul_id][time_key] = candidates
        battle_data.rogue_refresh_times[soul_id] = refresh_times
        global_data.emgr.rogue_gift_refresh.emit(soul_id, time_key, candidates)
        if global_data.player and soul_id == global_data.player.id:
            global_data.ui_mgr.close_ui('DeathRogueChooseUI')
            global_data.ui_mgr.show_ui('DeathRogueChooseUI', 'logic.comsys.battle.Death')

    @rpc_method(CLIENT_STUB, ())
    def enable_outer_base_rogue(self):
        if global_data.death_battle_data:
            global_data.death_battle_data.enable_out_base_rogue = True
        global_data.emgr.rogue_gift_enable_out_base_choose.emit()