# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/editor_utils/local_editor_utils.py
from __future__ import absolute_import
from mobile.common.mobilecommon import Singleton
from .mecha_weapons_skills_params import weapons_skills_params
from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_WEAPON_SFX, MECHA_FASHION_KEY
from logic.gutils.dress_utils import DEFAULT_CLOTHING_ID
from mobile.common.EntityFactory import EntityFactory

class LocalEditorData(Singleton):

    def __init__(self):
        self.role_id = None
        self.mecha_id = 8001
        self.mecha_skin_id = DEFAULT_CLOTHING_ID
        self.mecha_shiny_weapon_id = None
        return


class LocalEditor(Singleton):

    def __init__(self):
        self.data = LocalEditorData()
        self.mecha = None
        self.mecha_last_skin_info = None
        self.avatar = None
        self.initialize()
        return

    def initialize(self):
        global_data.local_battle_const.ensure_open_all_mecha()
        global_data.local_battle_const.ensure_open_all_mecha_skin()
        avatar = EntityFactory.instance().create_entity('Avatar', global_data.local_battle_const.AVATAR_EID)
        global_data.player = avatar
        avatar.init_from_dict(global_data.local_battle_const.avatar_init_data)
        self.avatar = avatar
        avatar.local_soul_create_entity('SurvivalBattle', global_data.local_battle_const.battle_init_data, global_data.local_battle_const.BATTLE_EID)

    def add_avatar(self):
        global_data.battle.local_add_entity(global_data.local_battle_const.AVATAR_EID, 1, global_data.local_battle_const.battle_avatar_update_data)

    def remove_avatar(self):
        if not self.avatar:
            return
        cur_player_pos = self.avatar.logic.ev_g_position()
        avatar_data = global_data.local_battle_const.battle_avatar_update_data
        avatar_data['position'] = [cur_player_pos.x, cur_player_pos.y, cur_player_pos.z]
        avatar_data['mp_attr']['human_yaw'] = self.avatar.logic.ev_g_yaw()
        global_data.battle.local_remove_entity(global_data.local_battle_const.AVATAR_EID)

    def add_mecha(self, mecha_id, mecha_position_tuple, mecha_yaw, skin_info):
        if self.mecha:
            return
        else:
            if skin_info is None:
                skin_info = self.mecha_last_skin_info
            else:
                self.mecha_last_skin_info = skin_info
            mecha_init_data = global_data.local_battle_const.mecha_init_data
            mecha_init_data['npc_id'] = mecha_init_data['mecha_id'] = mecha_id
            mecha_init_data['weapons'] = weapons_skills_params[mecha_id]['weapons']
            mecha_init_data['skills'] = weapons_skills_params[mecha_id]['skills']
            mecha_init_data[MECHA_FASHION_KEY] = skin_info['mecha_fashion']
            mecha_init_data['position'] = mecha_position_tuple
            mecha_init_data['mp_attr']['human_yaw'] = mecha_yaw
            self.mecha = global_data.battle.create_entity('Mecha', global_data.local_battle_const.MECHA_EID, 1, mecha_init_data)
            return

    def remove_mecha(self):
        if not self.mecha:
            return
        else:
            global_data.battle.destroy_entity(global_data.local_battle_const.MECHA_EID)
            self.mecha = None
            return

    def reset(self):
        self.remove_avatar()
        self.remove_mecha()
        self.add_avatar()