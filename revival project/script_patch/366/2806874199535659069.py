# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8006.py
from __future__ import absolute_import
from .ComGenericMechaEffect import ComGenericMechaEffect
from logic.gcommon.const import PART_WEAPON_POS_MAIN1
FIRE_ANIM_NAME = 'shoot'
FIRE_EFFECT_ID = '11'
FIRE_EFFECT_INDEX = {800601: 0,
   800603: 1
   }
CURE_STATE_ID = 'bird_cure'
BIRD_CURE_EFFECT_ID = '12'
SUB_MODEL_KEY = 'ribbon'

class ComMechaEffect8006(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_WEAPON_DATA_CHANGED_SUCCESS': 'on_refresh_fire_effect_path',
       'E_SHOW_BIRD_CURE_EFFECT': 'on_show_bird_cure_effect',
       'E_ON_SKIN_SUB_MODEL_LOADED': 'on_skin_sub_model_loaded'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8006, self).init_from_dict(unit_obj, bdict)
        self.need_handle_anim = False

    def _get_specific_effect_path_from_list(self, effect_id, effect_path_list):
        if effect_id == FIRE_EFFECT_ID:
            obj_weapon = self.sd.ref_wp_bar_mp_weapons.get(PART_WEAPON_POS_MAIN1)
            weapon_id = obj_weapon.get_item_id()
            return effect_path_list[FIRE_EFFECT_INDEX[weapon_id]]

    def on_refresh_fire_effect_path(self, weapon_pos):
        if weapon_pos == PART_WEAPON_POS_MAIN1:
            self._fix_specific_anim_effect_info(FIRE_ANIM_NAME)

    def on_show_bird_cure_effect(self):
        self.on_trigger_state_effect(CURE_STATE_ID, BIRD_CURE_EFFECT_ID, True)

    def on_skin_sub_model_loaded(self):
        self.need_handle_anim = self.ev_g_mecha_fashion_id() in (201800655, )

    def on_trigger_anim_effect(self, anim_name, part, force_trigger_effect=False, socket_index=-1):
        super(ComMechaEffect8006, self).on_trigger_anim_effect(anim_name, part, force_trigger_effect, socket_index)
        if self.need_handle_anim:
            self.sd.ref_socket_res_agent.play_model_res_anim('idle' if anim_name != 'idle' else 'idle_default', SUB_MODEL_KEY)