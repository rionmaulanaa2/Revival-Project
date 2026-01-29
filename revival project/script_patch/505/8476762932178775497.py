# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8011.py
from __future__ import absolute_import
from .ComGenericMechaEffect import ComGenericMechaEffect
ABSORB_SHIELD_HIT_EFFECT_ID = '99'

class ComMechaEffect8011(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_SHOW_ABSORB_SHIELD_HIT_EFFECT': 'on_show_absorb_shield_hit_effect',
       'E_TRANS_TO_DRAGON': 'on_switch_dragon_shape'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8011, self).init_from_dict(unit_obj, bdict)

    def on_show_absorb_shield_hit_effect(self, pos, rot):
        self.on_trigger_disposable_effect(ABSORB_SHIELD_HIT_EFFECT_ID, pos, rot)

    def on_switch_dragon_shape(self, data, left_time):
        is_dragon_shape = left_time > 0
        self.sd.ref_socket_res_agent.set_model_res_visible(is_dragon_shape, 'dragon_shape')
        self.sd.ref_socket_res_agent.set_sfx_res_visible(is_dragon_shape, 'dragon_shape')
        self.sd.ref_socket_res_agent.set_sfx_res_visible(not is_dragon_shape, 'common_shape')