# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8009.py
from __future__ import absolute_import
from .ComGenericMechaEffect import ComGenericMechaEffect
from logic.gcommon.const import PART_WEAPON_POS_MAIN5, PART_WEAPON_POS_MAIN6
from logic.gcommon.common_const.mecha_const import TRIO_STATE_M, TRIO_STATE_S, TRIO_STATE_R
from logic.gutils.mecha_skin_utils import DEFAULT_RES_KEY
from logic.gcommon.common_const.character_anim_const import UP_BODY
import world
NEED_SYNC_WEAPON_POS_SET = {
 PART_WEAPON_POS_MAIN5, PART_WEAPON_POS_MAIN6}
WEAPON_POS_FIRE_STATE_MAP = {PART_WEAPON_POS_MAIN5: ('shotgun', '27'),
   PART_WEAPON_POS_MAIN6: ('rocket', '28')
   }
LETTER_STATE_ID = 'letter'
LETTER_EFFECT_ID_MAP = {TRIO_STATE_M: '18',
   TRIO_STATE_S: '19',
   TRIO_STATE_R: '20',
   'FullForce': '21'
   }
WEAPON_BUFF_STATE_ID = 'weapon_buff'
WEAPON_BUFF_EFFECT_ID_MAP = {TRIO_STATE_M: '22',
   TRIO_STATE_S: '23',
   TRIO_STATE_R: '24'
   }
FULL_FORCE_STATE_ID = 'full_force'
STATE_NO_FULL_FORCE = 0
STATE_FULL_FORCE_BEGIN = 1
STATE_FULL_FORCE_END = 2
FULL_FORCE_EFFECT_ID_MAP = {STATE_NO_FULL_FORCE: '',
   STATE_FULL_FORCE_BEGIN: '25',
   STATE_FULL_FORCE_END: '26'
   }
SPEED_INCREASE_BUFF_ID = 428
SUB_MODEL_KEY = 'weapon'

class ComMechaEffect8009(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_MODEL_LOADED': 'on_model_loaded',
       'E_GUN_ATTACK': 'on_gun_attack_start',
       'E_SWITCH_LETTER_EFFECT': 'on_switch_letter_sfx',
       'E_SWITCH_FULL_FORCE_EFFECT': 'on_switch_full_force_sfx',
       'E_SHOW_SHOT_SPEED_INCREASE_EFFECT': 'on_show_shot_speed_increase_effect',
       'E_SHOW_SPEED_SCALE_INCREASE_EFFECT': 'on_show_speed_scale_increase_effect',
       'E_SHOW_INJURY_DECREASE_EFFECT': 'on_show_injury_decrease_effect',
       'E_ON_SKIN_SUB_MODEL_LOADED': 'on_skin_sub_model_loaded'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8009, self).init_from_dict(unit_obj, bdict)
        self._cur_state = bdict.get('trio_state', TRIO_STATE_M)
        self._full_force_enabled = bdict.get('trio_firepower', False)
        self._full_force_state = STATE_FULL_FORCE_BEGIN if bdict.get('trio_firepower', False) else STATE_NO_FULL_FORCE
        self._weapon_buff_sfx = {TRIO_STATE_M: None,
           TRIO_STATE_S: None,
           TRIO_STATE_R: None
           }
        self.need_handle_anim = False
        return

    def on_model_loaded(self, model):
        super(ComMechaEffect8009, self).on_model_loaded(model)
        self.on_switch_letter_sfx('FullForce' if self._full_force_enabled else self._cur_state)
        self.on_switch_full_force_sfx(self._full_force_state)

    def on_trigger_anim_effect(self, anim_name, part, force_trigger_effect=False, socket_index=-1):
        super(ComMechaEffect8009, self).on_trigger_anim_effect(anim_name, part, force_trigger_effect, socket_index)
        if self.need_handle_anim:
            if anim_name == 'huoliquankai_01_sm01':
                self.sd.ref_socket_res_agent.set_model_res_visible(True, SUB_MODEL_KEY)
                self.sd.ref_socket_res_agent.play_model_res_anim((
                 'huoliquankai_01_sm01', -1, world.TRANSIT_TYPE_DEFAULT, 0, world.PLAY_FLAG_NO_LOOP, self.sd.ref_anim_rate[UP_BODY]), SUB_MODEL_KEY)
            elif anim_name == 'huoliquankai_03_sm01':
                self.sd.ref_socket_res_agent.set_model_res_visible(False, SUB_MODEL_KEY)

    def on_gun_attack_start(self, *args, **kwargs):
        socket_name, weapon_pos = args
        if weapon_pos in NEED_SYNC_WEAPON_POS_SET:
            socket_index = self.ev_g_fired_socket_index(weapon_pos)
            self.on_trigger_state_effect(force=True, socket_index=socket_index, need_sync=True, *WEAPON_POS_FIRE_STATE_MAP[weapon_pos])

    def on_switch_letter_sfx(self, state):
        self._cur_state = state
        self.on_trigger_state_effect(LETTER_STATE_ID, LETTER_EFFECT_ID_MAP[state], need_sync=True)

    def on_switch_full_force_sfx(self, state):
        self._full_force_state = state
        self.on_trigger_state_effect(FULL_FORCE_STATE_ID, FULL_FORCE_EFFECT_ID_MAP[state], need_sync=True)

    def _on_show_weapon_buff_effect(self, buff_type, flag):
        state_id = WEAPON_BUFF_STATE_ID + buff_type
        effect_id = WEAPON_BUFF_EFFECT_ID_MAP[buff_type] if flag else ''
        self.on_trigger_state_effect(state_id, effect_id)

    def on_show_shot_speed_increase_effect(self, flag):
        self._on_show_weapon_buff_effect(TRIO_STATE_M, flag)

    def on_show_speed_scale_increase_effect(self, flag, buff_id):
        if buff_id == SPEED_INCREASE_BUFF_ID:
            self._on_show_weapon_buff_effect(TRIO_STATE_S, flag)

    def on_show_injury_decrease_effect(self, flag):
        self._on_show_weapon_buff_effect(TRIO_STATE_R, flag)

    def on_skin_sub_model_loaded(self):
        self.need_handle_anim = self.ev_g_mecha_fashion_id() == 201800941