# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/AssaultBattle.py
from __future__ import absolute_import
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.entities.DeathBattle import DeathBattle
from logic.gcommon.common_const.battle_const import ASSAULT_ENEMY_PLAYER_TIP, ASSAULT_GAME_START_TIP, ASSAULT_TEAMMATE_PLAYER_TIP, MED_NODE_RECRUIT_COMMON_INFO, MAIN_NODE_COMMON_INFO
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool, Tuple
ASSAULT_ST_PLAYERS_SHORTAGE = 1
ASSAULT_ST_FACTION_SHORTAGE = 2
ASSAULT_ST_NORMAL = 3
ROOM_CLOSE_REASON_TEXT = {ASSAULT_ST_FACTION_SHORTAGE: 18345,
   ASSAULT_ST_PLAYERS_SHORTAGE: 18344
   }

class AssaultBattle(DeathBattle):

    def __init__(self, entityid):
        super(AssaultBattle, self).__init__(entityid)
        self.force_trigger_door = True

    def init_from_dict(self, bdict, is_change_weapon=True):
        super(AssaultBattle, self).init_from_dict(bdict)
        self._join_score_dict = bdict.get('join_score_dict', {})
        self._join_soul_score_dict = bdict.get('join_soul_score_dict', {})
        self._join_soul_assist_dict = bdict.get('join_soul_assist_dict', {})
        self._join_soul_dmg_dict = bdict.get('join_soul_dmg_dict', {})
        self._is_support_surrender = False

    def load_finish(self):
        super(AssaultBattle, self).load_finish()

    @rpc_method(CLIENT_STUB, (Str('char_name'), Int('group_id'), Bool('state'), Uuid('entity_id')))
    def notify_players_change(self, char_name, group_id, state, entity_id):
        if not global_data.cam_lplayer:
            return
        if global_data.cam_lplayer.ev_g_group_id() == group_id:
            tip_type = ASSAULT_TEAMMATE_PLAYER_TIP
        else:
            tip_type = ASSAULT_ENEMY_PLAYER_TIP
        if state:
            content_txt = get_text_by_id(18338)
        else:
            content_txt = get_text_by_id(18339)
            self.pop_join_soul_data(entity_id)
        message = {'i_type': tip_type,'content_txt': content_txt.format(name=char_name)}
        global_data.emgr.show_battle_main_message.emit(message, MAIN_NODE_COMMON_INFO, False, False)

    @rpc_method(CLIENT_STUB, (Float('end_timestamp'), Int('reason')))
    def notify_assault_finish(self, end_timestamp, reason):
        if reason == 0:
            return
        if reason == ASSAULT_ST_NORMAL:
            global_data.emgr.hide_assault_room_close_tips.emit()
        else:
            global_data.emgr.show_assault_room_close_tips.emit(end_timestamp, ROOM_CLOSE_REASON_TEXT.get(int(reason), 18344))

    @rpc_method(CLIENT_STUB, ())
    def notify_assault_force_quit(self):
        self.has_quit = True

    def show_battle_start_tips(self):
        tip_type = ASSAULT_GAME_START_TIP
        message = {'i_type': tip_type,'content_txt': 19707}
        global_data.emgr.show_battle_med_message.emit((message,), MED_NODE_RECRUIT_COMMON_INFO)

    def get_enter_group_data(self, player_id):
        return self._join_score_dict.get(player_id, {})

    def get_join_soul_point_data(self):
        return self._join_soul_score_dict

    def get_join_soul_assist_data(self):
        return self._join_soul_assist_dict

    def get_join_soul_dmg_data(self):
        return self._join_soul_dmg_dict

    def pop_join_soul_data(self, entity_id):
        join_soul_score_dict = self._join_soul_score_dict.get(global_data.cam_lplayer.id, {})
        if entity_id in join_soul_score_dict:
            join_soul_score_dict.pop(entity_id)
        join_soul_assist_dict = self._join_soul_assist_dict.get(global_data.cam_lplayer.id, {})
        if entity_id in join_soul_assist_dict:
            join_soul_assist_dict.pop(entity_id)
        join_soul_dmg_dict = self._join_soul_dmg_dict.get(global_data.cam_lplayer.id, {})
        if entity_id in join_soul_dmg_dict:
            join_soul_dmg_dict.pop(entity_id)

    def destroy(self, clear_cache=True):
        super(AssaultBattle, self).destroy(clear_cache)

    def on_update_group_points(self, group_id, point):
        pass

    def _refresh_mvp_mark(self, mvp_id):
        pass

    def need_skip_end_exp_ui(self):
        return True