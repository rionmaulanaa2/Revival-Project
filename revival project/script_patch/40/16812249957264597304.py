# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/RecruitmentSurvivalBattle.py
from __future__ import absolute_import
import six_ex
from logic.entities.SurvivalBattle import SurvivalBattle
from logic.gcommon.common_const import battle_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool, Tuple

class RecruitmentSurvivalBattle(SurvivalBattle):

    def __init__(self, *args, **kwargs):
        super(RecruitmentSurvivalBattle, self).__init__(*args, **kwargs)

    def send_player_recruit_message(self, player_id, recruit_type, player_name=''):
        ent = global_data.battle.get_entity(player_id)
        if ent is None:
            player_char_name = player_name
        else:
            player_char_name = ent.logic.ev_g_char_name()
        text_id = {battle_const.RECRUITMENT_BATTLE_LEAVE: 83164,battle_const.RECRUITMENT_BATTLE_REJECT: 83165,
           battle_const.RECRUITMENT_BATTLE_ACCEPT: 83166
           }
        msg = {'i_type': recruit_type,
           'content_txt': get_text_by_id(text_id.get(recruit_type, battle_const.RECRUITMENT_BATTLE_LEAVE)).format(player_char_name),
           'extra_disappear_time': 2
           }
        global_data.emgr.show_battle_med_message.emit((msg,), battle_const.MED_NODE_RECRUIT_COMMON_INFO)
        return

    def show_accept_and_leave_message(self, lst_member_order_dict, now_member_order_dict, member_id, player_name=''):
        lst_teammate_set = set(six_ex.keys(lst_member_order_dict))
        now_teammate_set = set(six_ex.keys(now_member_order_dict))
        leave_teammates = lst_teammate_set - now_teammate_set
        if member_id in leave_teammates:
            self.send_player_recruit_message(member_id, battle_const.RECRUITMENT_BATTLE_LEAVE, player_name)
        enter_teammates = now_teammate_set - lst_teammate_set
        if member_id in enter_teammates:
            self.send_player_recruit_message(member_id, battle_const.RECRUITMENT_BATTLE_ACCEPT, player_name)

    def recruit_valid(self):
        return True

    @rpc_method(CLIENT_STUB, (Dict('member_order_dict'), Uuid('member_id')))
    def refresh_group_orders(self, member_order_dict, member_id):
        lplayer = global_data.cam_lplayer
        if not lplayer or not lplayer.is_valid():
            return
        lplayer.send_event('E_REFRESH_GROUP_ORDERS', member_order_dict, member_id)