# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8002.py
from __future__ import absolute_import
import six
from .ComGenericMechaEffect import ComGenericMechaEffect
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gcommon.const import SOUND_TYPE_MECHA_FIRE, SOUND_TYPE_MECHA_FOOTSTEP
from logic.gcommon.common_const.character_anim_const import LOW_BODY
import world
MULTIPLE_JUMP_SOUND = {1: [
     'm_8002_jump', 'nf'],
   2: [
     'm_8002_jump2', 'nf']
   }
SWORD_CORE_STATE_ID = 'sword_core'
SWORD_CORE_EFFECT_ID_MAP = {True: '99',
   False: ''
   }
SUB_MODEL_KEY = 'cape'

class ComMechaEffect8002(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_SHOW_SOWRD_CORE_EFFECT': 'on_show_sword_core_effect',
       'E_JUMP_STAGE': 'on_multiple_jump_stage',
       'E_SWORD_ENERGY_FIRE': 'on_sword_fire',
       'E_ON_SKIN_SUB_MODEL_LOADED': 'on_skin_sub_model_loaded'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8002, self).init_from_dict(unit_obj, bdict)
        self.need_handle_anim = False
        self.need_play_idle_anim = False

    def on_show_sword_core_effect(self, show):
        self.on_trigger_state_effect(SWORD_CORE_STATE_ID, SWORD_CORE_EFFECT_ID_MAP[show])

    def on_multiple_jump_stage(self, jump_stage):
        if jump_stage in six.iterkeys(MULTIPLE_JUMP_SOUND):
            sound_name = MULTIPLE_JUMP_SOUND[jump_stage]
            self.play_and_bcast_sound(sound_name, SOUND_TYPE_MECHA_FOOTSTEP)

    def on_sword_fire(self, sub_state):
        self.play_and_bcast_sound(['m_8002_weapon2_fire', 'nf'], SOUND_TYPE_MECHA_FIRE)

    def play_and_bcast_sound(self, sound_name, sound_visible_type=SOUND_TYPE_MECHA_FOOTSTEP):
        self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 1, sound_name, 0, 0, 1, sound_visible_type)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_EXECUTE_MECHA_ACTION_SOUND, (1, sound_name, 0, 0, 1, sound_visible_type)], True)

    def on_skin_sub_model_loaded(self):
        self.need_handle_anim = self.ev_g_mecha_fashion_id() in (201800254, 201800255,
                                                                 201800256)

    def on_trigger_anim_effect(self, anim_name, part, force_trigger_effect=False, socket_index=-1):
        super(ComMechaEffect8002, self).on_trigger_anim_effect(anim_name, part, force_trigger_effect, socket_index)
        if self.need_handle_anim:
            if anim_name and 'thrust_land_' in anim_name:
                self.sd.ref_socket_res_agent.play_model_res_anim((
                 anim_name, -1, world.TRANSIT_TYPE_DEFAULT, 0, world.PLAY_FLAG_NO_LOOP, self.sd.ref_anim_rate[LOW_BODY]), SUB_MODEL_KEY)
                self.need_play_idle_anim = True
            elif self.need_play_idle_anim:
                self.need_play_idle_anim = False
                self.sd.ref_socket_res_agent.play_model_res_anim((
                 'idle', -1, world.TRANSIT_TYPE_DEFAULT, 0, world.PLAY_FLAG_LOOP, self.sd.ref_anim_rate[LOW_BODY]), SUB_MODEL_KEY)