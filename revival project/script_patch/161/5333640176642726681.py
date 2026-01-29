# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8014.py
from __future__ import absolute_import
from .ComGenericMechaEffect import ComGenericMechaEffect
BLADE_SLASH_HIT_EFFECT_ID = '18'
BLADE_SLASH_HIT_SCREEN_EFFECT_ID = '19'
BLADE_SHOW_STATE_ID = 'blade_show'
BLADE_SHOW_EFFECT_ID_MAP = {True: '20',
   False: '21'
   }
BLADE_HIT_STATE_ID = 'hit_effect'
BLADE_MODEL_KEY = 'blade'

class ComMechaEffect8014(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_SHOW_SLASH_HIT_SFX': 'on_show_blade_slash_hit_sfx',
       'E_SHOW_SLASH_HIT_SCREEN_SFX': 'on_show_blade_slash_hit_screen_sfx',
       'E_SLASH_ACTIVATED': 'on_slash_activated',
       'E_ON_SKIN_SFX_LOADED': 'on_mecha_sfx_loaded',
       'E_POST_ACTION': 'on_play_slash_anim'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8014, self).init_from_dict(unit_obj, bdict)
        self.slash_activated = False

    def on_show_blade_slash_hit_sfx(self, pos, rot=None):
        self.on_trigger_disposable_effect(BLADE_SLASH_HIT_EFFECT_ID, pos, rot, need_sync=True)

    def on_show_blade_slash_hit_screen_sfx(self):
        self.on_trigger_state_effect(BLADE_HIT_STATE_ID, BLADE_SLASH_HIT_SCREEN_EFFECT_ID, force=True, need_sync=True)

    def on_slash_activated(self, flag, duration=0.0):
        if self.slash_activated ^ flag:
            self.on_trigger_state_effect(BLADE_SHOW_STATE_ID, BLADE_SHOW_EFFECT_ID_MAP[flag], force=True, need_sync=True)
            self.sd.ref_socket_res_agent.set_model_res_visible(flag, BLADE_MODEL_KEY)
            self.sd.ref_socket_res_agent.set_sfx_res_visible(flag, BLADE_MODEL_KEY)
            self.slash_activated = flag