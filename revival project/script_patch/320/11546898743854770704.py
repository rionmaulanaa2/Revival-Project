# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/KingBattle.py
from __future__ import absolute_import
import six
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool, Tuple
from logic.comsys.battle.King.KingBattleData import KingBattleData
from logic.entities.Battle import Battle
from logic.gcommon.common_const import battle_const
from logic.gcommon.common_const import shop_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.client.const import koth_shop_const
from logic.gcommon.common_const import battle_achieve_const
ACHIEVE_SCORE_TIPS = {battle_achieve_const.KING_BATTLE_ACHIEVE_SCORE_CHANGE_REASON_DAMAGE_TO_PLAYER: battle_const.MAIN_KOTH_DAMAGE_POINT,
   battle_achieve_const.KING_BATTLE_ACHIEVE_SCORE_CHANGE_REASON_DAMAGE_TO_MECHA: battle_const.MAIN_KOTH_DAMAGE_POINT,
   battle_achieve_const.KING_BATTLE_ACHIEVE_SCORE_CHANGE_REASON_RESCUE_GROUPMATE: battle_const.MAIN_KOTH_RESCUE_POINT,
   battle_achieve_const.KING_BATTLE_ACHIEVE_SCORE_CHANGE_REASON_KILL_PLAYER: battle_const.MAIN_KOTH_KILL_POINT,
   battle_achieve_const.KING_BATTLE_ACHIEVE_SCORE_CHANGE_REASON_KILL_MECHA: battle_const.MAIN_KOTH_KILL_MECHA_POINT,
   battle_achieve_const.KING_BATTLE_ACHIEVE_SCORE_CHANGE_REASON_REVENGE: battle_const.MAIN_KOTH_REVENGE_POINT,
   battle_achieve_const.KING_BATTLE_ACHIEVE_SCORE_CHANGE_REASON_END_COMBO_KILL: battle_const.MAIN_KOTH_END_COMBO_KILL_POINT,
   battle_achieve_const.KING_BATTLE_ACHIEVE_SCORE_CHANGE_REASON_COMBO_KILL: battle_const.MAIN_KOTH_COMBO_KILL_POINT,
   battle_achieve_const.KING_BATTLE_ACHIEVE_SCORE_CHANGE_REASON_OCCUPY_BEACON_TOWER: battle_const.MAIN_KOTH_OCCUPY_POINT,
   battle_achieve_const.KING_BATTLE_ACHIEVE_SCORE_CHANGE_REASON_GRAP_KING_POINT: battle_const.MAIN_KOTH_OCCUPY_POINT
   }
TURN_TIPS = {battle_const.KOTH_BATTLE_TIP_TYPE_ROUND_WARN_TIME: battle_const.UP_NODE_TURN_WARN,
   battle_const.KOTH_BATTLE_TIP_TYPE_ROUND_COUNTDOWN_TIME: battle_const.UP_NODE_TURN_COUNTDOWN,
   battle_const.KOTH_BATTLE_TIP_TYPE_ROUND_SPECIAL_REWARD_RATE: battle_const.MAIN_NODE_SPECIAL_POINT,
   battle_const.KOTH_BATTLE_TIP_TYPE_ROUND_BEGIN: battle_const.MAIN_NODE_SPECIAL_POINT
   }

class KingBattle(Battle):

    def init_from_dict(self, bdict):
        super(KingBattle, self).init_from_dict(bdict)
        my_faction_id = bdict.get('faction_id', {})
        KingBattleData().set_my_camp_id(my_faction_id)
        KingBattleData().init_camps()
        KingBattleData().init_occupys()

    def init_battle_scene(self, scene_data):
        self.load_scene(scene_data)

    @rpc_method(CLIENT_STUB, (Dict('faction_points_dict'), Dict('faction_status_dict')))
    def update_battle_data(self, faction_points_dict, faction_status_dict):
        self.update_faction_point((faction_points_dict,))
        self.update_faction_status((faction_status_dict,))

    @rpc_method(CLIENT_STUB, (Dict('faction_points_dict'),))
    def update_faction_point(self, faction_points_dict):
        if not global_data.king_battle_data:
            return
        for faction_id, faction_point in six.iteritems(faction_points_dict):
            global_data.king_battle_data.update_camp_point(faction_id, faction_point)

    @rpc_method(CLIENT_STUB, (Dict('faction_status_dict'),))
    def update_faction_status(self, faction_status_dict):
        global_data.king_battle_data and global_data.king_battle_data.update_camp_status(faction_status_dict)

    @rpc_method(CLIENT_STUB, (List('king_status_list'),))
    def update_king_status(self, king_status_list):
        global_data.king_battle_data and global_data.king_battle_data.update_occupy_status(king_status_list)

    @rpc_method(CLIENT_STUB, (Uuid('entity_id'), Dict('money_dict'), Int('reason')))
    def update_player_money(self, entity_id, money_dict, reason):
        self.on_update_player_money(entity_id, money_dict, reason)

    @rpc_method(CLIENT_STUB, (Uuid('entity_id'), Float('cd')))
    def update_player_fill_all_bullets_cd(self, entity_id, cd):
        self.on_update_player_fill_all_bullets_cd(entity_id, cd)

    @rpc_method(CLIENT_STUB, (Uuid('entity_id'), Int('achievement_id')))
    def on_player_get_achievement(self, entity_id, achievement_id):
        pass

    def _get_combo_kill_tips_id(self, combo_kill_num):
        if combo_kill_num:
            tips_id = 8200 + combo_kill_num - 2
            if tips_id < 8201:
                return 8201
            else:
                if tips_id > 8206:
                    return 8206
                return tips_id

        return 8201

    @rpc_method(CLIENT_STUB, (Uuid('entity_id'), Int('change_num'), Int('now_num'), Int('reason'), Dict('extra_info_dict')))
    def update_player_achieve_score(self, entity_id, change_num, now_num, reason, extra_info_dict):
        if reason in ACHIEVE_SCORE_TIPS:
            i_type = ACHIEVE_SCORE_TIPS[reason]
            msg = {'i_type': i_type
               }
            is_owner = True if global_data.cam_lplayer and global_data.cam_lplayer.id == entity_id else False
            if i_type == battle_const.MAIN_KOTH_END_COMBO_KILL_POINT:
                if extra_info_dict:
                    if is_owner:
                        msg_owner = {'i_type': i_type,'show_num': change_num,
                           'cur_point': now_num
                           }
                        global_data.cam_lplayer.send_event('E_SHOW_MAIN_BATTLE_MESSAGE', msg_owner, battle_const.MAIN_NODE_POINT)
                        global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice',
                                                                               'even_kill_high'))
                    msg['i_type'] = battle_const.MAIN_KOTH_END_COMBO_KILL_POINT_ALL
                    msg['from_name'] = extra_info_dict['from']
                    msg['to_name'] = extra_info_dict['to']
                else:
                    msg['show_num'] = change_num
            elif i_type == battle_const.MAIN_KOTH_COMBO_KILL_POINT:
                if extra_info_dict:
                    tips_id = self._get_combo_kill_tips_id(extra_info_dict.get('combo_kill_num', None))
                    from_desc = get_text_by_id(tips_id)
                    if is_owner:
                        msg_owner = {'i_type': i_type,'show_num': change_num,
                           'cur_point': now_num,
                           'from_desc': from_desc
                           }
                        global_data.cam_lplayer.send_event('E_SHOW_MAIN_BATTLE_MESSAGE', msg_owner, battle_const.MAIN_NODE_POINT)
                        combo_kill_num = extra_info_dict.get('combo_kill_num', None)
                        if combo_kill_num is not None and combo_kill_num >= 3:
                            global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice',
                                                                                   'even_kill_high'))
                    msg['i_type'] = battle_const.MAIN_KOTH_COMBO_KILL_POINT_ALL
                    msg['from_name'] = '{0} {1}'.format(extra_info_dict['from'], from_desc)
                else:
                    msg['show_num'] = change_num
            else:
                msg['show_num'] = change_num
                if is_owner:
                    if i_type == battle_const.MAIN_KOTH_REVENGE_POINT:
                        global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice',
                                                                               'even_kill_high'))
                    elif i_type == battle_const.MAIN_KOTH_KILL_POINT:
                        global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice',
                                                                               'even_kill_low'))
            if is_owner:
                msg['cur_point'] = now_num
            global_data.cam_lplayer.send_event('E_SHOW_MAIN_BATTLE_MESSAGE', msg, battle_const.MAIN_NODE_POINT)
        return

    @rpc_method(CLIENT_STUB, (Dict('rank_data'),))
    def reply_rank_data(self, rank_data):
        global_data.king_battle_data and global_data.king_battle_data.update_rank_data(rank_data)

    @rpc_method(CLIENT_STUB, (Uuid('from_entity_id'), Uuid('to_entity_id'), Int('praised_num')))
    def update_player_been_praised_num(self, from_entity_id, to_entity_id, praised_num):
        global_data.king_battle_data and global_data.king_battle_data.update_like_data(to_entity_id, praised_num)
        global_data.emgr.update_koth_praised_num_event.emit(from_entity_id, to_entity_id, praised_num)

    def give_praise_for_player(self, to_player_id):
        if global_data.player and global_data.player.id != to_player_id:
            self.call_soul_method('give_praise_for_player', (to_player_id,))

    @rpc_method(CLIENT_STUB, (Int('point_id'), Dict('enemy_datas')))
    def update_king_point_area(self, point_id, enemy_datas):
        self.on_update_king_point_area(point_id, enemy_datas)

    def on_update_king_point_area(self, point_id, enemy_datas):
        global_data.king_battle_data.update_king_point_area(point_id, enemy_datas)
        global_data.emgr.update_king_point_area_event.emit(point_id, enemy_datas)

    def on_update_player_fill_all_bullets_cd(self, entity_id, cd):
        from logic.gcommon import time_utility
        global_data.king_battle_data.set_shop_bullet_cd(entity_id, cd + time_utility.get_server_time())
        if global_data.player and global_data.player.id == entity_id:
            global_data.emgr.update_koth_bullet_cd_info_event.emit(entity_id, cd)

    def on_update_player_money(self, entity_id, money_dict, reason):
        old_money_dict = global_data.king_battle_data.get_money_info(entity_id)
        global_data.king_battle_data.set_money_info(entity_id, money_dict)
        if global_data.cam_lplayer and global_data.cam_lplayer.id == entity_id:
            global_data.emgr.update_koth_money_info_event.emit(entity_id, money_dict)
            if reason in [shop_const.KING_SHOP_MONEY_CHANGE_REASON_SHOPPING]:
                global_data.game_mgr.show_tip(get_text_by_id(18214))
            if reason not in [shop_const.KING_SHOP_MONEY_CHANGE_REASON_INIT,
             shop_const.KING_SHOP_MONEY_CHANGE_REASON_SHOPPING,
             shop_const.KING_SHOP_MONEY_CHANGE_REASON_FACTION_REWARD_POINT,
             shop_const.KING_SHOP_MONEY_CHANGE_REASON_SYSTEM_SALARY]:
                gold = old_money_dict.get(shop_const.KING_SHOP_MONEY_UNIT_GOLD, 0)
                diamond = old_money_dict.get(shop_const.KING_SHOP_MONEY_UNIT_DIAMOND, 0)
                new_gold = money_dict.get(shop_const.KING_SHOP_MONEY_UNIT_GOLD, 0)
                new_diamond = money_dict.get(shop_const.KING_SHOP_MONEY_UNIT_DIAMOND, 0)
                gold_got = new_gold - gold
                diamond_got = new_diamond - diamond
                if gold_got > 0:
                    msg = {'msg': ''.join([get_text_by_id(18206).format(currency=get_text_by_id(25002)), ' + ', str(gold_got)]),'info': {'icon': koth_shop_const.GOLD_PIC,'size': (1.0, 1.0)}}
                    global_data.cam_lplayer.send_event('E_SHOW_BATTLE_MESSAGE_EVENT', msg, ignore_check=True)
                if diamond_got > 0:
                    msg = {'msg': ''.join([get_text_by_id(18206).format(currency=get_text_by_id(25001)), ' + ', str(diamond_got)]),'info': {'icon': koth_shop_const.DIAMOND_PIC,'size': (1.0, 1.0)}}
                    global_data.cam_lplayer.send_event('E_SHOW_BATTLE_MESSAGE_EVENT', msg, ignore_check=True)

    @rpc_method(CLIENT_STUB, (Dict('beacon_tower_dict'),))
    def update_beacon_tower_mark(self, beacon_tower_dict):
        global_data.king_battle_data.update_beacon_tower_info(beacon_tower_dict)
        for entity_id, beacon_tower_info in six.iteritems(beacon_tower_dict):
            global_data.emgr.update_beacon_tower_mark_event.emit(entity_id, beacon_tower_info)

    @rpc_method(CLIENT_STUB, (Int('round_num'), Int('tip_type'), Dict('tip_info')))
    def show_battle_tips(self, round_num, tip_type, tip_info):
        if tip_type in (battle_const.KOTH_BATTLE_TIP_TYPE_ROUND_WARN_TIME, battle_const.KOTH_BATTLE_TIP_TYPE_ROUND_COUNTDOWN_TIME):
            if round_num == 5 and tip_type == battle_const.KOTH_BATTLE_TIP_TYPE_ROUND_COUNTDOWN_TIME:
                tip_info = [battle_const.KOTH_BATTLE_TIP_ROUND_FINISH_TIME_LAST_ROUND_COUNT_DOWN_TIME, tip_info]
                global_data.emgr.show_battle_med_message.emit(tip_info, battle_const.MED_NODE_TURN_COUNTDOWN)
            else:
                tip_info['i_type'] = tip_type
                global_data.emgr.battle_event_message.emit(tip_info, message_type=TURN_TIPS[tip_type])
        elif tip_type == battle_const.KOTH_BATTLE_TIP_TYPE_ROUND_SPECIAL_REWARD_RATE:
            global_data.emgr.show_battle_main_message.emit(tip_info, TURN_TIPS[tip_type])
        else:
            global_data.emgr.show_battle_main_message.emit({'i_type': battle_const.MAIN_ACE_TIME}, message_type=battle_const.MAIN_NODE_COMMON_INFO)
            global_data.emgr.show_battle_main_message.emit(tip_info, TURN_TIPS[tip_type])