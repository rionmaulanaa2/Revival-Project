# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8029.py
from __future__ import absolute_import
from .ComGenericMechaEffect import ComGenericMechaEffect
from logic.gcommon.common_utils.bcast_utils import E_REFRESH_WEAPON_STATE, E_REFRESH_SUB_MODEL_ANIM
from logic.gcommon.common_const.mecha_const import STATE_VISIBLE
TRANSLATION_SFX = '104'
TRANSLATION_SCREEN_STATE_ID = 'translation_screen'
TRANSLATION_SCREEN_EFFECT_ID = '105'
TRANSLATION_SELF_SFX = '107'
TRANSLATION_SELF_STATE_ID = 'translation_self'
PHANTOM_SELF_SFX = '108'
PHANTOM_SELF_STATE_ID = 'phantom_self'

class ComMechaEffect8029(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_REFRESH_WEAPON_STATE': 'refresh_weapon_model',
       'E_UPDATE_TRANSLATION_SCREEN_SFX': 'update_translation_screen_sfx',
       'E_BEGIN_PHANTIOM_SFX': 'begin_phantom_sfx',
       'E_UPDATE_TRANSLATION_SFX': 'update_translation_sfx',
       'E_REFRESH_SUB_MODEL_ANIM': 'set_sub_model_anim'
       })

    def refresh_weapon_model(self, state):
        state_list = STATE_VISIBLE[state]
        for vis_state in state_list[0]:
            self.sd.ref_socket_res_agent.set_model_res_visible(True, vis_state)

        for invis_state in state_list[1]:
            self.sd.ref_socket_res_agent.set_model_res_visible(False, invis_state)

        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_REFRESH_WEAPON_STATE, (state,)], True)

    def update_translation_screen_sfx(self, flag):
        effect_id = TRANSLATION_SCREEN_EFFECT_ID if flag else ''
        self.on_trigger_state_effect(TRANSLATION_SCREEN_STATE_ID, effect_id, force=True)

    def begin_phantom_sfx(self):
        self.on_trigger_state_effect(PHANTOM_SELF_STATE_ID, PHANTOM_SELF_SFX, True)

    def update_translation_sfx(self, pos):
        self.on_trigger_disposable_effect(TRANSLATION_SFX, (pos.x, pos.y, pos.z), need_sync=True)
        self.on_trigger_state_effect(PHANTOM_SELF_SFX, TRANSLATION_SELF_SFX, True)

    def set_sub_model_anim(self, anim, key):
        self.sd.ref_socket_res_agent.play_model_res_anim(anim, key)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [E_REFRESH_SUB_MODEL_ANIM, (anim, key)], True)