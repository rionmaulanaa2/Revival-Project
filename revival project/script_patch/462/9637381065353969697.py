# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/OccupyBattle.py
from __future__ import absolute_import
import six
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool
from logic.entities.DeathBattle import DeathBattle
from logic.gcommon.common_const.battle_const import MUTIOCCUPY_BECOME_KING, MUTIOCCUPY_USE_ITEM, MAIN_NODE_COMMON_INFO, TDM_FIRST_POINTS_TIPS_THRE, TDM_RED_FIRST_ARRIVE_40_POINT, TDM_BLUE_FIRST_ARRIVE_40_POINT
from logic.gutils.item_utils import check_use_mechatran_card_valid
import world

class OccupyBattle(DeathBattle):

    def init_from_dict(self, bdict, is_change_weapon=True):
        super(OccupyBattle, self).init_from_dict(bdict, is_change_weapon)
        self._item_score = bdict.get('occupy_item_score', 0)
        self._armor_score = bdict.get('occupy_armor_score', 0)
        global_data.death_battle_data and global_data.death_battle_data.init_occupy_data(bdict.get('control_point_info', {}))

    @rpc_method(CLIENT_STUB, (Float('settle_timestamp'), List('born_point_list'), Dict('group_born_dict'), Dict('control_point_dict'), Dict('group_points_dict'), Dict('selected_combat_weapons')))
    def update_battle_data(self, settle_timestamp, born_point_list, group_born_dict, control_point_dict, group_points_dict, selected_combat_weapons):
        self._update_battle_data(settle_timestamp, born_point_list, group_born_dict, group_points_dict, selected_combat_weapons)
        self.update_control_point((control_point_dict,))

    @rpc_method(CLIENT_STUB, (Dict('control_point_dict'),))
    def update_control_point(self, control_point_dict):
        global_data.death_battle_data and global_data.death_battle_data.update_occupy_point_info(control_point_dict)

    @rpc_method(CLIENT_STUB, (Dict('group_points_dict'),))
    def update_group_points(self, group_points_dict):
        if global_data.death_battle_data:
            old_group_points_dict = dict(global_data.death_battle_data.get_group_score_data())
        else:
            old_group_points_dict = {}
        if old_group_points_dict:
            self.on_update_group_points(old_group_points_dict, group_points_dict)
        global_data.death_battle_data and global_data.death_battle_data.update_group_score_data(group_points_dict)

    @rpc_method(CLIENT_STUB, (List('point_pos'), Float('delay_time')))
    def notify_control_point(self, point_pos, delay_time):
        pass

    @rpc_method(CLIENT_STUB, (Bool('result'),))
    def start_combat_result(self, result):
        if result:
            global_data.ui_mgr.close_ui('MutiOccupyDeathPlayBackUI')
            global_data.ui_mgr.close_ui('MutiOccupyBornChooseUI')

    def start_combat(self, born_pos=-1):
        self.call_soul_method('start_combat', (born_pos,))

    @rpc_method(CLIENT_STUB, (Str('names'), Int('text_id')))
    def notify_random_item(self, names, text_id):
        msg = get_text_by_id(text_id).format(name=names)
        message = {'i_type': MUTIOCCUPY_USE_ITEM,'content_txt': msg}
        message_type = MAIN_NODE_COMMON_INFO
        global_data.emgr.show_battle_main_message.emit(message, message_type, True, False)

    @rpc_method(CLIENT_STUB, (Str('names'),))
    def notify_groupmate_got_item(self, names):
        msg = get_text_by_id(17448).format(name=names)
        message = {'i_type': MUTIOCCUPY_BECOME_KING,'content_txt': msg}
        message_type = MAIN_NODE_COMMON_INFO
        global_data.emgr.show_battle_main_message.emit(message, message_type, True, False)

    @rpc_method(CLIENT_STUB, (Int('score'),))
    def update_occupy_item_score(self, score):
        self._item_score = score
        global_data.emgr.update_occupy_points_self.emit()

    @rpc_method(CLIENT_STUB, (Int('score'),))
    def update_occupy_armor_score(self, score):
        self._armor_score = score
        global_data.emgr.update_occupy_points_self.emit()

    def use_occupy_item(self):
        extra_info = {}
        player = global_data.cam_lplayer
        if player:
            pos = player.ev_g_position()
            scn = world.get_active_scene()
            exclude_ids = player.ev_g_human_col_id()
            can_use_mecha, pos = check_use_mechatran_card_valid(scn, pos, exclude_ids)
            if can_use_mecha:
                extra_info['position'] = (
                 pos.x, pos.y, pos.z)
        self.call_soul_method('use_occupy_item', (extra_info,))

    def on_update_group_points(self, old_group_points_dict, group_points_dict):
        TIPS_THRE = 1600
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
                    text = get_text_by_id(17462).format(score=TIPS_THRE)
                    msg = {'i_type': TDM_BLUE_FIRST_ARRIVE_40_POINT,
                       'content_txt': text
                       }
                else:
                    text = get_text_by_id(17463).format(score=TIPS_THRE)
                    msg = {'i_type': TDM_RED_FIRST_ARRIVE_40_POINT,
                       'content_txt': text
                       }
            if msg:
                global_data.cam_lplayer.send_event('E_SHOW_MAIN_BATTLE_MESSAGE', msg, MAIN_NODE_COMMON_INFO)
            return