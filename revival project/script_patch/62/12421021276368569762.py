# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8017.py
from __future__ import absolute_import
from .ComGenericMechaEffect import ComGenericMechaEffect
from logic.gcommon.const import PART_WEAPON_POS_MAIN1
import logic.gcommon.common_utils.bcast_utils as bcast
import math3d
import world
MAIN_WEAPON_ENHANCE_STATE_ID = 'enhance'
MAIN_WEAPON_ENHANCE_EFFECT_ID_MAP = {True: '99',
   False: ''
   }
MAIN_WEAPON_FIRE_STATE_ID = 'fire'
MAIN_WEAPON_FIRE_EFFECT_ID = '100'
MAIN_WEAPON_SPLIT_STATE_ID = 'split'
MAIN_WEAPON_SPLIT_EFFECT_ID_MAP = {True: '101',
   False: ''
   }

class ComMechaEffect8017(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ENHANCE_MAIN_WEAPON': 'on_enhance_main_weapon',
       'E_GUN_ATTACK': 'on_gun_attack_start',
       'E_SHOW_SPLIT_MAIN_WEAPON': 'on_show_split_main_weapon',
       'E_SUSPEND_RADIAL_WEAPON': 'on_suspend_radial_weapon',
       'E_SET_SUSPEND_RADIAL_WEAPON_POSITION': 'set_suspend_radial_weapon_position',
       'G_SUSPEND_RADIAL_WEAPON_POSITION': 'get_suspend_radial_weapon_position'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8017, self).init_from_dict(unit_obj, bdict)
        self.sd.ref_radial_weapon_suspended = False
        self.sd.ref_radial_weapon_suspended_position = None
        return

    def on_model_loaded(self, model):
        super(ComMechaEffect8017, self).on_model_loaded(model)
        if self.ev_g_is_avatar():
            self.on_show_split_main_weapon(False)

    def on_enhance_main_weapon(self, flag):
        self.on_trigger_state_effect(MAIN_WEAPON_ENHANCE_STATE_ID, MAIN_WEAPON_ENHANCE_EFFECT_ID_MAP[flag])

    def on_gun_attack_start(self, socket_name, weapon_pos):
        if weapon_pos == PART_WEAPON_POS_MAIN1:
            self.on_trigger_state_effect(MAIN_WEAPON_FIRE_STATE_ID, MAIN_WEAPON_FIRE_EFFECT_ID, force=True, need_sync=True)

    def on_show_split_main_weapon(self, flag):
        self.on_trigger_state_effect(MAIN_WEAPON_SPLIT_STATE_ID, MAIN_WEAPON_SPLIT_EFFECT_ID_MAP[flag], need_sync=True)

    def on_suspend_radial_weapon(self, flag):
        self.sd.ref_radial_weapon_suspended = flag
        if not flag:
            self.set_suspend_radial_weapon_position(None)
        return

    def set_suspend_radial_weapon_position(self, position):
        if position is not None:
            self.sd.ref_radial_weapon_suspended_position = math3d.vector(*position)
        else:
            self.sd.ref_radial_weapon_suspended_position = None
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SET_SUSPEND_RADIAL_WEAPON_POSITION, (position,)], True)
        return