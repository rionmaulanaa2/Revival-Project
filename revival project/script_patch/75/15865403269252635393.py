# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8025.py
from __future__ import absolute_import
from .ComGenericMechaEffect import ComGenericMechaEffect
SECOND_WEAPON_EFFECT_STATE_ID = {0: 'second_weapon_1',
   1: 'second_weapon_2',
   2: 'second_weapon_3',
   3: 'second_weapon_4'
   }
SECOND_WEAPON_HOLD_STATE_EFFECT_MAP = {0: '100',
   1: '101',
   2: '102',
   3: '103'
   }
SECOND_WEAPON_FIRE_STATE_EFFECT_MAP = {0: '104',
   1: '105',
   2: '106',
   3: '107'
   }

class ComMechaEffect8025(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_PLAY_SECOND_WEAPON_HOLD_EFFECT': 'play_second_weapon_hold_effect',
       'E_STOP_SECOND_WEAPON_HOLD_EFFECT': 'stop_second_weapon_hold_effect',
       'E_PLAY_SECOND_WEAPON_FIRE_EFFECT': 'play_second_weapon_fire_effect',
       'E_ON_SKIN_SUB_MODEL_LOADED': 'skin_sub_model_loaded'
       })

    def play_second_weapon_hold_effect(self, index_list):
        for index in index_list:
            self.on_trigger_state_effect(SECOND_WEAPON_EFFECT_STATE_ID[index], SECOND_WEAPON_HOLD_STATE_EFFECT_MAP[index], need_sync=True)

    def stop_second_weapon_hold_effect(self, index_list):
        for index in index_list:
            self.on_trigger_state_effect(SECOND_WEAPON_EFFECT_STATE_ID[index], '', need_sync=True)

    def play_second_weapon_fire_effect(self, index_list):
        for index in index_list:
            self.on_trigger_state_effect(SECOND_WEAPON_EFFECT_STATE_ID[index], SECOND_WEAPON_FIRE_STATE_EFFECT_MAP[index], force=True, need_sync=True)

    def skin_sub_model_loaded(self):
        skin_id = self.ev_g_mecha_fashion_id()
        if skin_id in (201802541, ):
            self.sd.ref_socket_res_agent.set_model_res_visible(True, 'battle_only')
            self.sd.ref_socket_res_agent.set_model_res_visible(False, 'lobby_only')