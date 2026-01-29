# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/CrownBattle.py
from __future__ import absolute_import
from logic.entities.DeathBattle import DeathBattle
from logic.gcommon.common_const import battle_const
from mobile.common.EntityManager import EntityManager
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool, Tuple
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from logic.gcommon.common_const.battle_const import CROWN_OTHER_FACTION, CROWN_SELF_FACTION, CROWN_TEAM_FACTION, MAIN_NODE_COMMON_INFO, CROWN_BATTLE_CROWN_TEAM_BORN_TIPS, CROWN_BATTLE_CROWN_OTHER_DIE_TIPS, CROWN_BATTLE_CROWN_OTHER_BORN_TIPS, CROWN_BATTLE_CROWN_TEAM_DIE_TIPS
CROWN_DIE_TIPS = {CROWN_OTHER_FACTION: CROWN_BATTLE_CROWN_OTHER_DIE_TIPS,
   CROWN_TEAM_FACTION: CROWN_BATTLE_CROWN_TEAM_DIE_TIPS,
   CROWN_SELF_FACTION: None
   }
CROWN_BORN_TIPS = {CROWN_OTHER_FACTION: CROWN_BATTLE_CROWN_OTHER_BORN_TIPS,
   CROWN_TEAM_FACTION: CROWN_BATTLE_CROWN_TEAM_BORN_TIPS,
   CROWN_SELF_FACTION: None
   }
HUMAN_CROWN_TIPS = {1: 17295,
   2: 17294,
   3: 17296
   }

class CrownBattle(DeathBattle):

    def init_from_dict(self, bdict):
        super(CrownBattle, self).init_from_dict(bdict)
        self.group_kind_id = bdict.get('group_kind_id', {})
        self.soul_crown_count = bdict.get('soul_crown_count', {})

    def load_finish(self):
        super(CrownBattle, self).load_finish()
        self.call_soul_method('request_crown_info_all', ())
        self.call_soul_method('request_remain_time', ())
        self.call_soul_method('request_crown_info', (global_data.player.id,))

    @rpc_method(CLIENT_STUB, (Uuid('king_id'), Int('alive_point')))
    def earn_alive_point(self, king_id, alive_point):
        global_data.game_mgr.show_tip('earn_alive_point %d' % alive_point)

    def get_real_faction(self, king_id, faction_id):
        if not global_data.player or not global_data.player.logic:
            return None
        else:
            if king_id == global_data.player.id:
                return CROWN_SELF_FACTION
            if faction_id == global_data.player.logic.ev_g_group_id():
                return CROWN_TEAM_FACTION
            return CROWN_OTHER_FACTION

    @rpc_method(CLIENT_STUB, (Uuid('king_id'), Int('king_faction')))
    def king_dead(self, king_id, king_faction):
        king_faction = self.get_real_faction(king_id, king_faction)
        if not king_faction:
            return
        global_data.emgr.on_crown_death.emit(king_id, king_faction)
        i_type = CROWN_DIE_TIPS[king_faction]
        if i_type:
            msg1 = {'i_type': i_type}
            message_type = MAIN_NODE_COMMON_INFO
            global_data.emgr.show_battle_main_message.emit(msg1, message_type, False, False)

    @rpc_method(CLIENT_STUB, (Uuid('new_king_id'), Int('king_faction')))
    def new_king_appear(self, new_king_id, king_faction):
        king_faction = self.get_real_faction(new_king_id, king_faction)
        if not king_faction:
            return
        self.group_kind_id[king_faction] = new_king_id
        global_data.emgr.on_crown_born.emit(new_king_id, king_faction)
        i_type = CROWN_BORN_TIPS[king_faction]
        if i_type:
            msg1 = {'i_type': i_type}
            message_type = MAIN_NODE_COMMON_INFO
            global_data.emgr.show_battle_main_message.emit(msg1, message_type, False, False)
        self.show_guide_tips(king_faction)

    @rpc_method(CLIENT_STUB, (Uuid('soul_id'), Int('crown_count')))
    def update_crown_count(self, soul_id, crown_count):
        self.soul_crown_count[soul_id] = crown_count
        if global_data.cam_lplayer and soul_id == global_data.cam_lplayer.id:
            global_data.emgr.update_crown_count.emit(crown_count)

    @rpc_method(CLIENT_STUB, (Uuid('soul_id'), Int('crown_count'), Bool('is_king')))
    def reply_crown_info(self, soul_id, crown_count, is_king):
        self.soul_crown_count[soul_id] = crown_count
        if global_data.cam_lplayer and soul_id == global_data.cam_lplayer.id:
            global_data.emgr.update_crown_count.emit(crown_count)
            if is_king:
                global_data.emgr.on_crown_born.emit(soul_id, CROWN_SELF_FACTION)
            else:
                global_data.emgr.on_crown_death.emit(soul_id, CROWN_SELF_FACTION)

    @rpc_method(CLIENT_STUB, (List('crown_info'),))
    def reply_crown_info_all(self, crown_info):
        global_data.emgr.on_crown_death.emit(None, CROWN_OTHER_FACTION)
        global_data.emgr.on_crown_death.emit(None, CROWN_TEAM_FACTION)
        global_data.emgr.on_crown_death.emit(None, CROWN_SELF_FACTION)
        for info in crown_info:
            if info[2] == True:
                entity = EntityManager.getentity(info[0])
                if global_data.player.id == info[0]:
                    faction_id = CROWN_SELF_FACTION
                elif info[3] == global_data.player.logic.ev_g_group_id():
                    faction_id = CROWN_TEAM_FACTION
                else:
                    faction_id = CROWN_OTHER_FACTION
                global_data.emgr.on_crown_born.emit(info[0], faction_id)
            self.soul_crown_count[info[0]] = info[1]
            if global_data.cam_lplayer and info[0] == global_data.cam_lplayer.id:
                global_data.emgr.update_crown_count.emit(info[1])

        return

    @rpc_method(CLIENT_STUB, (Int('new_identity'),))
    def allocate_new_identity(self, new_identity):
        pass

    @rpc_method(CLIENT_STUB, (Int('remain_time'),))
    def update_king_alive_remaining_time(self, remain_time):
        global_data.emgr.update_king_alive_time.emit(remain_time)

    @rpc_method(CLIENT_STUB, (Int('remain_time'),))
    def become_pre_king(self, remain_time):
        global_data.emgr.become_pre_king.emit(remain_time)

    @rpc_method(CLIENT_STUB, ())
    def no_more_pre_king(self):
        global_data.emgr.no_more_pre_king.emit()

    def show_guide_tips(self, faction_id):
        if global_data.player:
            show_crown_guide_name = self.__class__.__name__ + str(HUMAN_CROWN_TIPS[faction_id]) + str(global_data.player.uid)
            show_guide = global_data.achi_mgr.get_cur_user_archive_data(show_crown_guide_name, False)
            if not show_guide:
                message_data = {'content_txt': get_text_by_id(HUMAN_CROWN_TIPS[faction_id]),'delay_time': 8,'template_scale': [0.8, 0.8]}
                global_data.emgr.battle_event_message.emit(message_data, message_type=battle_const.UP_NODE_COMMON_RIKO_TIPS)
                global_data.achi_mgr.set_cur_user_archive_data(show_crown_guide_name, True)

    def get_group_king_id(self):
        return self.group_kind_id

    def get_soul_crown_count(self, soul_id):
        return self.soul_crown_count.get(soul_id)